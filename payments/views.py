# payments/views.py
import json
import logging
from django.db import transaction
from django.utils import timezone
from datetime import date, timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from lib.models import Loan, LoanItem, Book
from .models import Payment
from .serializers import LoanRequestSerializer, PaymentSerializer
from .services.paystack_service import (
    initialize_transaction,
    verify_transaction,
    verify_webhook_signature
)
from django.conf import settings

logger = logging.getLogger(__name__)


# ── VIEW 1: INITIALIZE PAYMENT ───────────────────────
# Member hits this when they click "Borrow & Pay"
# ─────────────────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_loan_payment(request):
    """
    Member selects books → this view:
    1. Validates books are available
    2. Creates Loan (status=pending_payment)
    3. Creates LoanItems (books reserved)
    4. Creates Payment record
    5. Calls Paystack initialize
    6. Returns authorization_url to frontend
    """
    serializer = LoanRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    book_ids = [item['book_id'] for item in serializer.validated_data['books']]
    books = Book.objects.filter(id__in=book_ids)

    # ── CALCULATE AMOUNT ─────────────────────────────
    # 50 KES per book — comes from settings so you can
    # change it in one place without touching code
    # ─────────────────────────────────────────────────
    price_per_book = settings.LOAN_PRICE_KES
    total_amount = price_per_book * len(book_ids)

    # ── ATOMIC TRANSACTION ───────────────────────────
    # Everything below either ALL succeeds or ALL fails.
    # If Paystack call fails, Loan and Payment are rolled back.
    # No orphaned records in DB.
    # ─────────────────────────────────────────────────
    with transaction.atomic():

        # create loan — NOT activated yet
        loan = Loan.objects.create(
            borrower=request.user,
            status='pending_payment',       # member hasn't paid yet
            due_date=date.today() + timedelta(days=14)  # 2 week loan period
        )

        # create loan items — books are RESERVED, not decremented
        for book in books:
            LoanItem.objects.create(
                loan=loan,
                book=book
            )

        # create payment record BEFORE calling Paystack
        # WHY: if Paystack call fails after saving,
        # you have a record to debug. If you create payment
        # after Paystack responds, a network timeout means
        # Paystack has a payment but you have no record.
        payment = Payment.objects.create(
            user=request.user,
            loan=loan,
            expected_amount=total_amount
            # reference is auto-generated in model.save()
        )

        # ── CALL PAYSTACK ────────────────────────────
        # metadata = extra info you want visible
        # in your Paystack dashboard per transaction
        # ─────────────────────────────────────────────
        try:
            paystack_response = initialize_transaction(
                email=request.user.email,
                amount_kes=total_amount,
                reference=payment.reference,
                metadata={
                    'loan_id': loan.id,
                    'user_id': request.user.id,
                    'books': [b.title for b in books],
                    'book_count': len(book_ids)
                }
            )
        except Exception as e:
            # Paystack call failed — atomic block rolls back
            # Loan, LoanItems, Payment all deleted automatically
            logger.error(f"Paystack initialize failed: {e}")
            raise  # re-raise so atomic() rolls back

    # ── RETURN TO FRONTEND ───────────────────────────
    # Frontend uses authorization_url to redirect member
    # reference is used later to verify payment
    # ─────────────────────────────────────────────────
    return Response({
        'authorization_url': paystack_response['authorization_url'],
        'reference': payment.reference,
        'amount': total_amount,
        'book_count': len(book_ids),
        'loan_id': loan.id,
        'message': f'Pay KES {total_amount} for {len(book_ids)} book(s)'
    }, status=201)


# ── VIEW 2: VERIFY PAYMENT ───────────────────────────
# Frontend calls this AFTER Paystack redirects back.
# Paystack redirects to: yourfrontend.com/payment/callback?reference=xxx
# Frontend extracts reference and POSTs it here.
# ─────────────────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_loan_payment(request):
    """
    Frontend sends reference after Paystack redirect.
    We verify with Paystack, then activate the loan.
    """
    reference = request.data.get('reference')

    if not reference:
        return Response({'error': 'Reference required'}, status=400)

    # ── FIND OUR PAYMENT RECORD ──────────────────────
    payment = Payment.objects.filter(
        reference=reference,
        user=request.user   # security: user can only verify their own payments
    ).select_related('loan').first()

    if not payment:
        return Response({'error': 'Payment not found'}, status=404)

    # ── IDEMPOTENCY CHECK ────────────────────────────
    # If frontend calls verify twice (user refreshes page),
    # don't process it again — just return current status.
    # This is idempotency: same input → same output,
    # no matter how many times you call it.
    # ─────────────────────────────────────────────────
    if payment.status == 'success':
        return Response({
            'message': 'Payment already verified',
            'status': 'success',
            'loan_id': payment.loan.id
        })

    # ── VERIFY WITH PAYSTACK ─────────────────────────
    try:
        result = verify_transaction(reference, float(payment.expected_amount))
    except Exception as e:
        logger.error(f"Paystack verify error for {reference}: {e}")
        return Response({'error': 'Verification failed. Try again.'}, status=500)

    if not result['verified']:
        # payment failed or amount mismatch
        payment.status = 'failed'
        payment.paystack_response = result['data']
        payment.save()

        # cancel the loan
        payment.loan.status = 'cancelled'
        payment.loan.save()

        logger.warning(f"Payment {reference} failed: {result['reason']}")
        return Response({
            'error': result['reason'],
            'status': 'failed'
        }, status=400)

    # ── PAYMENT CONFIRMED ────────────────────────────
    # Now and ONLY now do we:
    # 1. Activate the loan
    # 2. Decrement book copies
    # 3. Mark payment as success
    #
    # All in one atomic block — if any step fails,
    # everything rolls back. No partial fulfillment.
    # ─────────────────────────────────────────────────
    with transaction.atomic():
        # update payment
        payment.status = 'success'
        payment.amount_paid = result['amount_paid']
        payment.paid_at = timezone.now()
        payment.paystack_response = result['data']
        payment.save()

        # activate loan
        loan = payment.loan
        loan.status = 'borrowed'
        loan.save()

        # decrement book copies NOW (not before payment)
        for item in loan.items.select_related('book'):
            book = item.book
            book.available_copies -= 1
            book.save()

    logger.info(f"Payment {reference} verified. Loan {loan.id} activated.")

    return Response({
        'message': 'Payment successful. Books are yours for 14 days.',
        'status': 'success',
        'loan_id': loan.id,
        'amount_paid': result['amount_paid'],
        'due_date': payment.loan.due_date
    })


# ── VIEW 3: WEBHOOK ──────────────────────────────────
# Paystack calls THIS directly — not the member.
# This is your safety net:
# if member closes browser after paying but before
# verify runs, the webhook still activates their loan.
#
# IMPORTANT: this endpoint must be AllowAny
# because Paystack has no account on your system.
# Security comes from signature verification instead.
# ─────────────────────────────────────────────────────
@api_view(['POST'])
@permission_classes([AllowAny])
def paystack_webhook(request):
    """
    Paystack calls this directly when payment events happen.
    Must verify signature FIRST before doing anything.
    """
    # ── STEP 1: VERIFY SIGNATURE ─────────────────────
    # If signature missing or invalid → reject immediately.
    # Do not process. Do not log payment details.
    # ─────────────────────────────────────────────────
    signature = request.headers.get('x-paystack-signature', '')

    if not verify_webhook_signature(request.body, signature):
        logger.warning("Webhook received with invalid signature")
        return Response({'error': 'Invalid signature'}, status=401)

    # ── STEP 2: PARSE EVENT ──────────────────────────
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return Response({'error': 'Invalid JSON'}, status=400)

    event = payload.get('event')
    data = payload.get('data', {})

    logger.info(f"Webhook received: {event}")

    # ── STEP 3: HANDLE charge.success ────────────────
    # This fires when payment is confirmed.
    # We re-verify (never trust webhook alone) then fulfill.
    # ─────────────────────────────────────────────────
    if event == 'charge.success':
        reference = data.get('reference')

        payment = Payment.objects.filter(reference=reference).first()

        if not payment:
            logger.warning(f"Webhook: no payment found for reference {reference}")
            # return 200 anyway — Paystack will retry on non-200
            # you don't want infinite retries for unknown references
            return Response({'message': 'OK'})

        # ── IDEMPOTENCY ──────────────────────────────
        # Webhook might fire multiple times (Paystack retries).
        # If loan already activated — do nothing, return 200.
        # ─────────────────────────────────────────────
        if payment.status == 'success':
            logger.info(f"Webhook: payment {reference} already processed")
            return Response({'message': 'Already processed'})

        # verify amount from webhook data
        amount_paid_kes = data.get('amount', 0) / 100

        if amount_paid_kes < float(payment.expected_amount):
            logger.error(
                f"Webhook amount mismatch: "
                f"expected {payment.expected_amount}, got {amount_paid_kes}"
            )
            payment.status = 'failed'
            payment.save()
            return Response({'message': 'Amount mismatch logged'})

        # ── FULFILL ──────────────────────────────────
        with transaction.atomic():
            payment.status = 'success'
            payment.amount_paid = amount_paid_kes
            payment.paid_at = timezone.now()
            payment.paystack_response = data
            payment.save()

            loan = payment.loan
            loan.status = 'borrowed'
            loan.save()

            for item in loan.items.select_related('book'):
                book = item.book
                book.available_copies -= 1
                book.save()

        logger.info(f"Webhook: Loan {loan.id} activated via webhook")

    # ── ALWAYS RETURN 200 TO PAYSTACK ────────────────
    # If you return anything other than 200,
    # Paystack will keep retrying the webhook.
    # Even if you don't recognize the event — return 200.
    # ─────────────────────────────────────────────────
    return Response({'message': 'OK'})


# ── VIEW 4: PAYMENT HISTORY ──────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_history(request):
    """Member views their own payment history"""
    payments = Payment.objects.filter(
        user=request.user
    ).select_related('loan').order_by('-created_at')

    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)