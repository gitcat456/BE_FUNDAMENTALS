from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random

class User(AbstractUser):
    """Cusom User Model"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('librarian', 'Librarian'),
        ('member', 'Member'),
        ('customer', 'Customer')
    ]
    
    phone = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    
    #helper methods
    def is_admin(self):
        return self.role == 'admin'
    
    def is_librarian(self):
        return self.role == 'librarian'
    
    def can_manage_books(self):
        return self.is_admin() or self.is_librarian()
    
    def __str__(self):
        return self.username
    
    

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    photo_url = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True)
    
     # location fields
    location = models.CharField(max_length=255, blank=True, null=True)  # raw input
    place_name = models.CharField(max_length=255, blank=True, null=True)  # Mapbox cleaned
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    
     # Google Login fields
    google_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    auth_provider = models.CharField(
        max_length=20,
        choices=[('email', 'Email'), ('google', 'Google')],
        default='email'
    )
    
     # phone
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    phone_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profile"


class APIKey(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='api_keys',
        null=True,
        blank=True
    )
    
    name = models.CharField(max_length=100, help_text="e.g., Production Server")
    key = models.CharField(max_length=64, unique=True, db_index=True, blank=True)
    prefix = models.CharField(max_length=8, blank=True)
    scopes = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    @staticmethod
    def generate_key():
        return secrets.token_urlsafe(48)
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
            self.prefix = self.key[:8]
        super().save(*args, **kwargs)
    
    def is_valid(self):
        if not self.is_active:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True
    
    def __str__(self):
        return f"APIKey {self.prefix}... ({self.name})"
    

class AuthToken(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='auth_token'
    )
    key = models.CharField(max_length=40, unique=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Token for {self.user.username}"
    
    @staticmethod
    def generate_key():
        """Generate a random 40-character token"""
        return secrets.token_hex(20)  # 20 bytes = 40 hex chars
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)
    
class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(32)  # cryptographically secure
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=15)
        super().save(*args, **kwargs)

    def is_valid(self):
        return not self.used and timezone.now() < self.expires_at

    def __str__(self):
        return f"{self.user.username} - {'valid' if self.is_valid() else 'expired'}"    
    

class OTPVerification(models.Model):
    CHANNEL_CHOICES = [
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
    ]
    PURPOSE_CHOICES = [
        ('register', 'Registration'),
        ('login', 'Login'),
        ('password_reset', 'Password Reset'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    code = models.CharField(max_length=6)
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES)
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(random.randint(100000, 999999))  # 6-digit OTP
        if not self.expires_at:
            from django.utils import timezone
            from datetime import timedelta
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

    def is_valid(self):
        from django.utils import timezone
        return not self.verified and timezone.now() < self.expires_at

    def __str__(self):
        return f"{self.user.username} - {self.code} - {self.channel}"

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    available_copies = models.IntegerField()  # How many can be borrowed
    
    class Meta:
        permissions = [
            ("can_ban_book", "Can ban book from library"),
            ("can_feature_book", "Can feature book on Homepage"),
            ("can_bulk_import", "Can bulk import books"),
        ]
    
    def __str__(self):
        return f"{self.title}"
    
class RefreshToken(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='refresh_tokens'
    )
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    revoked = models.BooleanField(default=False)
    
    @staticmethod
    def generate_token():
        return secrets.token_hex(32)
    
    def is_expired(self):
     return self.expires_at < timezone.now()
    
    def is_valid(self):
     return not self.is_expired() and not self.revoked
    
    def __str__(self):
        return f"RefreshToken for {self.user.username}"
    
# class Member(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     membership_active = models.BooleanField(default=True)
    
class Loan(models.Model):
    borrower = models.ForeignKey(User, related_name='loans', on_delete=models.CASCADE, null=True)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[('borrowed', 'Borrowed'), ('returned', 'Returned')],
        default='borrowed'
    )
    
class LoanItem(models.Model):
    loan = models.ForeignKey(Loan, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
