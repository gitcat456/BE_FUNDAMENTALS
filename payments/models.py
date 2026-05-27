# payments/models.py
# ─────────────────────────────────────────────────────
# WHY A SEPARATE PAYMENT MODEL?
# The Loan tells you WHAT was borrowed.
# The Payment tells you WHAT MONEY MOVED.
# These are different concerns — keeping them separate
# means you can refund a payment without touching the loan,
# audit money without touching library logic, etc.
# ─────────────────────────────────────────────────────

from django.db import models
from django.conf import settings
import secrets


class Payment(models.Model):

    # ── STATUS CHOICES ──────────────────────────────
    # Every state a payment can be in.
    # pending    → initialized, customer hasn't paid yet
    # success    → money confirmed by Paystack verify + webhook
    # failed     → Paystack returned failed status
    # refunded   → money returned to customer
    # ────────────────────────────────────────────────
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    # the user making the payment
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    # ── WHY OneToOne WITH LOAN? ──────────────────────
    # One loan = one payment attempt at a time.
    # If payment fails, we cancel this loan and
    # member starts a fresh loan request.
    # Prevents one loan having multiple active payments.
    # ────────────────────────────────────────────────
    loan = models.OneToOneField(
        'lib.Loan',
        on_delete=models.CASCADE,
        related_name='payment'
    )

    # ── REFERENCE ───────────────────────────────────
    # This is YOUR tracking ID for this payment.
    # Sent to Paystack on initialize.
    # Comes back in webhook + verify response.
    # This is how you link Paystack events to YOUR records.
    # Must be unique — Paystack rejects duplicate references.
    # ────────────────────────────────────────────────
    reference = models.CharField(max_length=100, unique=True)

    # amount YOU expected to receive — in KES (whole number)
    # stored separately so you can detect amount mismatches
    expected_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # amount Paystack actually received — set after verification
    # if expected_amount != amount_paid → flag it, don't fulfill
    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # ── PAYSTACK_RESPONSE ───────────────────────────
    # Store the full Paystack API response as JSON.
    # WHY: if there's a dispute 6 months later,
    # you have the exact response Paystack sent you.
    # Audit trail. Non-negotiable.
    # ────────────────────────────────────────────────
    paystack_response = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # auto-generate unique reference if not set
        # format: LIB-{8 random chars} — readable in Paystack dashboard
        if not self.reference:
            self.reference = f"LIB-{secrets.token_hex(8).upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment {self.reference} - {self.status} - KES {self.expected_amount}"