from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(user):
    subject = "Welcome to the platform!"

    message = f"""
    Hi {user.username},

    Your account has been created successfully!.
    
    Welcome aboard.
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,  # raise error if sending fails
    )