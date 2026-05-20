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
    

def send_password_reset_email(user, token):
    reset_url = f"http://localhost:8000/api/auth/reset-password/?token={token}"
    
    subject = "Reset your password"
    message=f"""
    Hi {user.username},
    
    You requested a password reset.
    
    Click this link to reset your password (expires in 15 minutes)
    {reset_url}
    
    IF you didnt request this, ignore this email.
    Your password will not change.
    """
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,    
    )
    