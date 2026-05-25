from twilio.rest import Client
from django.conf import settings


def get_twilio_client():
    return Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


# ── SMS ──────────────────────────────────────────
def send_sms(to: str, message: str) -> dict:
    """
    Send plain SMS.
    to → phone number with country code e.g. +254712345678
    """
    client = get_twilio_client()

    try:
        msg = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to
        )
        return {'success': True, 'sid': msg.sid}
    except Exception as e:
        return {'success': False, 'error': str(e)}


# ── WHATSAPP ─────────────────────────────────────
def send_whatsapp(to: str, message: str) -> dict:
    """
    Send WhatsApp message via Twilio sandbox.
    to → phone number with country code e.g. +254712345678
    Twilio adds whatsapp: prefix automatically
    """
    client = get_twilio_client()

    try:
        msg = client.messages.create(
            body=message,
            from_=f"whatsapp:{settings.TWILIO_WHATSAPP_NUMBER}",
            to=f"whatsapp:{to}"
        )
        return {'success': True, 'sid': msg.sid}
    except Exception as e:
        return {'success': False, 'error': str(e)}


# ── OTP MESSAGES ─────────────────────────────────
def send_otp_sms(to: str, code: str, purpose: str) -> dict:
    purpose_text = {
        'register': 'verify your account',
        'login': 'log in',
        'password_reset': 'reset your password'
    }.get(purpose, 'continue')

    message = (
        f"Your YourApp verification code is: {code}\n"
        f"Use this to {purpose_text}.\n"
        f"Expires in 10 minutes. Do not share this code."
    )
    return send_sms(to, message)


def send_otp_whatsapp(to: str, code: str, purpose: str) -> dict:
    purpose_text = {
        'register': 'verify your account',
        'login': 'log in',
        'password_reset': 'reset your password'
    }.get(purpose, 'continue')

    message = (
        f"*YourApp Verification* 🔐\n\n"
        f"Your code is: *{code}*\n\n"
        f"Use this to {purpose_text}.\n"
        f"⏱ Expires in 10 minutes.\n\n"
        f"_Do not share this code with anyone._"
    )
    return send_whatsapp(to, message)


# ── ORDER NOTIFICATIONS ───────────────────────────
def send_order_update_whatsapp(to: str, order_id: int, status: str) -> dict:
    status_emoji = {
        'pending': '⏳',
        'paid': '✅',
        'shipped': '🚚',
        'delivered': '📦',
        'cancelled': '❌'
    }.get(status, '📋')

    message = (
        f"*YourApp Order Update* {status_emoji}\n\n"
        f"Order *#{order_id}* is now *{status.upper()}*.\n\n"
        f"Questions? Reply to this message."
    )
    return send_whatsapp(to, message)


def send_order_update_sms(to: str, order_id: int, status: str) -> dict:
    message = f"YourApp: Order #{order_id} is now {status.upper()}. Questions? Contact support."
    return send_sms(to, message)