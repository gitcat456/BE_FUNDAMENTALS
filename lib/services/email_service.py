from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_welcome_email(user):
    subject = "Welcome to Lib Desk!"
    
    #render template with context
    html_content = render_to_string('emails/welcome.html', {
        'username': user.username,
        'login_url': f"{settings.FRONTEND_URL}/login",
        'unsubscribe_url': f"{settings.FRONTEND_URL}/unsubscribe?email={user.email}",
    })
    
    # plain text fallback (always include this)
    text_content = f"Welcome {user.username}! Your account has been created."
    
     # EmailMultiAlternatives sends both HTML and plain text
    # email client picks whichever it supports
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content, #plain text version
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    email.attach_alternative(html_content, "text/html") #HTML version
    email.send()

    # message = f"""
    # Hi {user.username},

    # Your account has been created successfully!.
    
    # Welcome aboard.
    # """

    # send_mail(
    #     subject=subject,
    #     message=message,
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     recipient_list=[user.email],
    #     fail_silently=False,  # raise error if sending fails
    # )
    

def send_password_reset_email(user, token):
    reset_url = f"{settings.FRONTEND_URL.rstrip('/')}/reset-password?token={token}"
    
    subject = "Reset your password"
    
    html_content = render_to_string('emails/password_reset.html', {
        'username': user.username,
        'reset_url': reset_url,
    })
    
    text_content = f"Reset your password: {reset_url} (expires in 15 mins)"
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
     
    # message=f"""
    # Hi {user.username},
    
    # You requested a password reset.
    
    # Click this link to reset your password (expires in 15 minutes)
    # {reset_url}
    
    # IF you didnt request this, ignore this email.
    # Your password will not change.
    # """
    
    # send_mail(
    #     subject=subject,
    #     message=message,
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     recipient_list=[user.email],
    #     fail_silently=False,    
    # )
    
def send_order_confirmation_email(order):
    subject = f"Order Confirmed — {order.id}"

    items = order.items.all()

    TAX_RATE = 16
    subtotal = sum(item.quantity * item.price_at_purchase for item in items)
    tax = round(subtotal * TAX_RATE / 100, 2)
    total = round(subtotal + tax, 2)

    html_content = render_to_string('emails/order_confirmation.html', {
        'username': order.customer_email,   # no user FK, use email as name
        'order': order,
        'items': items,
        'subtotal': subtotal,
        'tax': tax,
        'tax_rate': TAX_RATE,
        'total': total,
        'order_url': f"{settings.FRONTEND_URL}/orders/{order.id}",
    })

    text_content = f"Order #{order.id} confirmed. Total: ${total}"

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[order.customer_email]           # directly from model
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    

def send_payment_receipt_email(user, payment, loan):
    subject = f"Payment Receipt — KES {payment.amount_paid}"

    html_content = render_to_string('emails/payment_receipt.html', {
        'username': user.username,
        'reference': payment.reference,
        'amount': payment.amount_paid,
        'loan_id': loan.id,
        'due_date': loan.due_date,
        'books': [item.book.title for item in loan.items.select_related('book')]
    })

    text_content = f"Payment of KES {payment.amount_paid} confirmed. Reference: {payment.reference}"

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()