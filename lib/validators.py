from django.core.exceptions import ValidationError
import re


class MinimumLengthValidator:
    """Password must be at least 8 characters"""
    
    def __init__(self, min_length=8):
        self.min_length = min_length
    
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                f"Password must be at least {self.min_length} characters long.",
                code='password_too_short',
            )
    
    def get_help_text(self):
        return f"Your password must contain at least {self.min_length} characters."


class UppercaseValidator:
    """Password must contain uppercase letter"""
    
    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                "Password must contain at least one uppercase letter.",
                code='password_no_upper',
            )
    
    def get_help_text(self):
        return "Your password must contain at least one uppercase letter."


class LowercaseValidator:
    """Password must contain lowercase letter"""
    
    def validate(self, password, user=None):
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                "Password must contain at least one lowercase letter.",
                code='password_no_lower',
            )
    
    def get_help_text(self):
        return "Your password must contain at least one lowercase letter."


class NumberValidator:
    """Password must contain a number"""
    
    def validate(self, password, user=None):
        if not re.search(r'\d', password):
            raise ValidationError(
                "Password must contain at least one number.",
                code='password_no_number',
            )
    
    def get_help_text(self):
        return "Your password must contain at least one number."


class SpecialCharacterValidator:
    """Password must contain special character"""
    
    def validate(self, password, user=None):
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                "Password must contain at least one special character.",
                code='password_no_special',
            )
    
    def get_help_text(self):
        return "Your password must contain at least one special character (!@#$%^&*...)."