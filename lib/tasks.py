# lib/tasks.py
# ─────────────────────────────────────────────────────
# Tasks are just Python functions decorated with @shared_task
# @shared_task → works regardless of Celery app name
#                portable, reusable across projects
#
# IMPORTANT RULE:
# Tasks must be IDEMPOTENT
# Running same task twice = same result as running once
# Why: Celery might retry failed tasks
# If task sends email → retry → sends email twice 💀
# Solution: check before acting, use idempotency keys
# ─────────────────────────────────────────────────────

from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,              # gives access to self (the task instance)
    max_retries=3,          # retry up to 3 times on failure
    default_retry_delay=60  # wait 60 seconds between retries
)
def send_welcome_email_task(self, user_id):
    """
    Send welcome email asynchronously.

    WHY user_id NOT user object?
    → Tasks are serialized to JSON for Redis
    → Django model objects can't be serialized to JSON
    → Always pass IDs, fetch the object inside the task
    → This also ensures you get fresh data from DB
    """
    try:
        from django.contrib.auth import get_user_model
        from lib.services.email_service import send_welcome_email

        User = get_user_model()
        user = User.objects.get(id=user_id)

        send_welcome_email(user)
        logger.info(f"Welcome email sent to {user.email}")

    except Exception as exc:
        logger.error(f"Welcome email failed for user {user_id}: {exc}")
        # retry the task with exponential backoff
        # attempt 1: retry in 60s
        # attempt 2: retry in 120s
        # attempt 3: retry in 240s
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_password_reset_email_task(self, user_id, token):
    """Send password reset email asynchronously."""
    try:
        from django.contrib.auth import get_user_model
        from lib.services.email_service import send_password_reset_email

        User = get_user_model()
        user = User.objects.get(id=user_id)

        send_password_reset_email(user, token)
        logger.info(f"Password reset email sent to {user.email}")

    except Exception as exc:
        logger.error(f"Password reset email failed for user {user_id}: {exc}")
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_payment_receipt_task(self, payment_id):
    """Send payment receipt email + SMS asynchronously."""
    try:
        from payments.models import Payment
        from lib.services.email_service import send_payment_receipt_email

        payment = Payment.objects.select_related('loan', 'user').get(id=payment_id)
        send_payment_receipt_email(
            user=payment.user,
            payment=payment,
            loan=payment.loan
        )
        logger.info(f"Receipt email sent for payment {payment.reference}")

    except Exception as exc:
        logger.error(f"Receipt email failed for payment {payment_id}: {exc}")
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
    
    

# ── LOAN DUE REMINDERS ───────────────────────────────
@shared_task(bind=True, max_retries=3)
def send_loan_due_reminders_task(self):
    """
    Runs every day at 8am.
    Finds all loans due tomorrow.
    Sends reminder email + SMS to each borrower.

    WHY TOMORROW NOT TODAY:
    → gives member time to return books
    → sending reminder on due date = too late
    → 1 day notice = actionable
    """
    try:
        from django.utils import timezone
        from datetime import timedelta
        from lib.models import Loan
        from lib.services.email_service import send_loan_reminder_email

        tomorrow = timezone.now().date() + timedelta(days=1)

        # find all active loans due tomorrow
        due_loans = Loan.objects.filter(
            status='borrowed',
            due_date=tomorrow
        ).select_related('borrower')

        count = 0
        for loan in due_loans:
            try:
                # fire individual task per loan
                # if one fails → others still send
                send_single_loan_reminder_task.delay(loan.id)
                count += 1
            except Exception as e:
                logger.error(f"Failed to queue reminder for loan {loan.id}: {e}")

        logger.info(f"Queued {count} loan reminders for {tomorrow}")

    except Exception as exc:
        logger.error(f"Loan reminder batch failed: {exc}")
        raise self.retry(exc=exc, countdown=300)  # retry in 5 mins


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_single_loan_reminder_task(self, loan_id):
    """
    Send reminder for ONE loan.
    Called by send_loan_due_reminders_task.

    WHY SPLIT INTO TWO TASKS?
    → batch task finds due loans (fast, no email sending)
    → individual tasks send emails (slow, retryable independently)
    → if 50 reminders needed and 3 fail → only 3 retry
      not all 50 retry
    → this pattern = fan-out
    """
    try:
        from lib.models import Loan, UserProfile
        from lib.services.email_service import send_loan_reminder_email

        loan = Loan.objects.select_related('borrower').get(id=loan_id)
        user = loan.borrower
        books = [item.book.title for item in loan.items.select_related('book')]

        # email reminder
        send_loan_reminder_email(user, loan, books)

        logger.info(f"Loan reminder sent to {user.username} for loan {loan_id}")

    except Exception as exc:
        logger.error(f"Loan reminder failed for loan {loan_id}: {exc}")
        raise self.retry(exc=exc)


# ── CLEANUP EXPIRED PASSWORD RESET TOKENS ────────────
@shared_task
def cleanup_expired_tokens_task():
    """
    Runs nightly at midnight.
    Deletes expired/used password reset tokens.

    WHY CLEAN UP?
    → tokens expire in 15 minutes
    → used tokens marked used=True
    → they pile up in DB forever if not cleaned
    → 1000 users/day = 1000 useless rows/day
    → this keeps DB lean

    NO RETRY NEEDED:
    → if it fails tonight → runs again tomorrow
    → cleanup tasks are naturally idempotent
    → running twice = same result as running once
    """
    from django.utils import timezone
    from lib.models import PasswordResetToken

    # delete tokens that are either:
    # → expired (created > 15 mins ago)
    # → already used
    deleted_count, _ = PasswordResetToken.objects.filter(
        expires_at__lt=timezone.now()
    ).delete()

    used_deleted, _ = PasswordResetToken.objects.filter(
        used=True
    ).delete()

    logger.info(
        f"Cleaned up {deleted_count} expired + "
        f"{used_deleted} used password reset tokens"
    )


# ── CLEANUP EXPIRED OTPS ─────────────────────────────
@shared_task
def cleanup_expired_otps_task():
    """
    Runs every hour.
    Deletes OTP records older than 1 hour.
    OTPs expire in 10 minutes — anything older is junk.
    """
    from django.utils import timezone
    from datetime import timedelta
    from lib.models import OTPVerification

    cutoff = timezone.now() - timedelta(hours=1)

    deleted_count, _ = OTPVerification.objects.filter(
        created_at__lt=cutoff
    ).delete()

    logger.info(f"Cleaned up {deleted_count} expired OTP records")