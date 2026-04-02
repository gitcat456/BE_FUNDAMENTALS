from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets
from django.conf import settings

class User(AbstractUser):
    """Cusom User Model"""
    
    phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return self.username
    

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

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    available_copies = models.IntegerField()  # How many can be borrowed
    
    def __str__(self):
        return f"{self.title}"
    
class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    membership_active = models.BooleanField(default=True)
    
class Loan(models.Model):
    member = models.ForeignKey(Member, related_name='loans', on_delete=models.CASCADE)
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
