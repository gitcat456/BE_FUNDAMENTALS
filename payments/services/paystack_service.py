# payments/services/paystack_service.py
# ─────────────────────────────────────────────────────
# ALL Paystack HTTP calls live here and ONLY here.
# Views never call requests.get/post directly.
# WHY: if Paystack changes their API tomorrow,
# you fix ONE file, not 10 views.
# ─────────────────────────────────────────────────────

import requests
import hashlib
import hmac
from django.conf import settings


# ── BASE CONFIG ─────────────────────────────────────
# Every Paystack request needs this header.
# FROM DOCS: Authorization: Bearer sk_test_xxx
# ────────────────────────────────────────────────────
PAYSTACK_BASE_URL = "https://api.paystack.co"

def get_headers():
    return {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }


# ── AMOUNT HELPER ────────────────────────────────────
# FROM DOCS: amount must be in KOBO (smallest currency unit)
# KES 200 = 20000 kobo
# This is the #1 mistake developers make.
# Always convert through this function — never manually.
# ─────────────────────────────────────────────────────
def to_kobo(amount_kes: float) -> int:
    return int(amount_kes * 100)


# ── INITIALIZE ──────────────────────────────────────
# FROM PAYSTACK DOCS:
# POST https://api.paystack.co/transaction/initialize
# Body: { email, amount (kobo), reference, metadata }
# Returns: { authorization_url, access_code, reference }
#
# WHAT WE DO WITH THE RESPONSE:
# → save reference to Payment record (already done before calling this)
# → return authorization_url to frontend
# → frontend redirects member to that URL
# ─────────────────────────────────────────────────────
def initialize_transaction(email: str, amount_kes: float, reference: str, metadata: dict = None) -> dict:
    """
    Start a payment session with Paystack.
    Returns authorization_url for frontend redirect.
    """
    payload = {
        "email": email,
        "amount": to_kobo(amount_kes),    # ← always convert to kobo
        "reference": reference,             # ← YOUR reference, not Paystack's
        "currency": "KES",
        "callback_url": settings.PAYSTACK_CALLBACK_URL,
        "metadata": metadata or {}          # ← attach order context for your records
    }

    response = requests.post(
        f"{PAYSTACK_BASE_URL}/transaction/initialize",
        json=payload,
        headers=get_headers()
    )

    data = response.json()

    # ── READING THE RESPONSE ────────────────────────
    # data = {
    #   "status": true,          ← outer status: did the API call succeed?
    #   "message": "...",
    #   "data": {
    #     "authorization_url":   ← send this to frontend
    #     "access_code":         ← not needed for basic flow
    #     "reference":           ← confirm it matches what you sent
    #   }
    # }
    # ────────────────────────────────────────────────

    if not data.get('status'):
        # API call itself failed (wrong key, network issue etc.)
        raise Exception(f"Paystack initialize failed: {data.get('message')}")

    return {
        'authorization_url': data['data']['authorization_url'],
        'reference': data['data']['reference'],
        'access_code': data['data']['access_code']
    }


# ── VERIFY ──────────────────────────────────────────
# FROM PAYSTACK DOCS:
# GET https://api.paystack.co/transaction/verify/{reference}
# Returns full transaction details
#
# CRITICAL CHECKS (most devs skip these and get exploited):
# 1. data.status === 'success'     ← not outer status
# 2. data.amount === expected      ← attacker could pay KES 1
# 3. data.currency === 'KES'       ← currency match
# ─────────────────────────────────────────────────────
def verify_transaction(reference: str, expected_amount_kes: float) -> dict:
    """
    Verify a payment actually succeeded and amount is correct.
    Never trust the frontend saying 'payment was successful'.
    Always call this yourself.
    """
    response = requests.get(
        f"{PAYSTACK_BASE_URL}/transaction/verify/{reference}",
        headers=get_headers()
    )

    data = response.json()

    if not data.get('status'):
        raise Exception(f"Paystack verify failed: {data.get('message')}")

    transaction = data['data']

    # ── CHECK 1: payment status ──────────────────────
    # data['data']['status'] is the TRANSACTION status
    # completely different from outer data['status']
    # ─────────────────────────────────────────────────
    if transaction['status'] != 'success':
        return {
            'verified': False,
            'reason': f"Transaction status is {transaction['status']}",
            'data': transaction
        }

    # ── CHECK 2: amount match ────────────────────────
    # Convert back from kobo to KES for comparison.
    # If a member was supposed to pay 100 KES (2 books)
    # but only 50 KES arrived — do NOT fulfill the loan.
    # ─────────────────────────────────────────────────
    amount_paid_kes = transaction['amount'] / 100
    if amount_paid_kes < expected_amount_kes:
        return {
            'verified': False,
            'reason': f"Amount mismatch. Expected KES {expected_amount_kes}, got KES {amount_paid_kes}",
            'data': transaction
        }

    # ── CHECK 3: currency ────────────────────────────
    if transaction.get('currency') != 'KES':
        return {
            'verified': False,
            'reason': f"Currency mismatch: {transaction.get('currency')}",
            'data': transaction
        }

    return {
        'verified': True,
        'amount_paid': amount_paid_kes,
        'paid_at': transaction.get('paid_at'),
        'data': transaction  # store full response for audit
    }


# ── WEBHOOK SIGNATURE VERIFICATION ──────────────────
# FROM PAYSTACK DOCS:
# Paystack signs every webhook with your secret key.
# Header: x-paystack-signature = HMAC SHA512 of body
#
# WHY THIS MATTERS:
# Without this check, anyone can POST to your webhook
# and fake a successful payment for any order.
# This is the #1 security hole in payment integrations.
# ─────────────────────────────────────────────────────
def verify_webhook_signature(payload_bytes: bytes, signature: str) -> bool:
    """
    Verify that the webhook actually came from Paystack.
    payload_bytes → raw request.body (must be bytes, not parsed JSON)
    signature     → request.headers.get('x-paystack-signature')
    """
    expected_signature = hmac.new(
        key=settings.PAYSTACK_SECRET_KEY.encode('utf-8'),
        msg=payload_bytes,          
        digestmod=hashlib.sha512
    ).hexdigest()

    # use hmac.compare_digest — timing-safe comparison
    # regular == is vulnerable to timing attacks
    return hmac.compare_digest(expected_signature, signature)