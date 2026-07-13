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