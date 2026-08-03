# payments/tasks.py
from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def cancel_stale_payments_task():
    """
    Runs every hour at :30.
    Finds loans stuck in pending_payment for > 1 hour.
    Cancels them and frees up book copies.

    WHY THIS MATTERS:
    → member starts checkout → abandons payment
    → loan stays pending_payment forever
    → books are reserved but not borrowed
    → other members can't borrow those books
    → this releases stuck inventory automatically

    1 HOUR GRACE PERIOD:
    → generous enough for slow connections
    → tight enough to release inventory quickly
    """
    from django.utils import timezone
    from datetime import timedelta
    from lib.models import Loan

    cutoff = timezone.now() - timedelta(hours=1)

    # find loans stuck in pending_payment for over an hour
    stale_loans = Loan.objects.filter(
        status='pending_payment',
        borrowed_date__lt=cutoff
    ).select_related('payment')

    cancelled_count = 0
    for loan in stale_loans:
        try:
            loan.status = 'cancelled'
            loan.save()

            # mark payment as failed if exists
            if hasattr(loan, 'payment'):
                loan.payment.status = 'failed'
                loan.payment.save()

            cancelled_count += 1
            logger.info(f"Cancelled stale loan {loan.id}")

        except Exception as e:
            logger.error(f"Failed to cancel stale loan {loan.id}: {e}")

    logger.info(f"Cancelled {cancelled_count} stale pending payments")