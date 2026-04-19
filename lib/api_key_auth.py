from rest_framework import authentication, exceptions
from django.utils import timezone
from .models import APIKey


class APIKeyAuthentication(authentication.BaseAuthentication):
    """
    API Key authentication
    
    Clients send: Authorization: ApiKey abc123xyz
    """
    
    keyword = 'ApiKey'
    
    def authenticate(self, request):
        """Authenticate using API key"""
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return None
        
        if not auth_header.startswith(f'{self.keyword} '):
            return None
        
        # Extract key with validation
        parts = auth_header.split(' ')
        if len(parts) != 2:
            raise exceptions.AuthenticationFailed('Invalid API key format')
        
        api_key_string = parts[1]
        
        # Look up key in database
        try:
            api_key = APIKey.objects.get(key=api_key_string)
        except APIKey.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid API key')
        
        # Check if key is valid (active and not expired)
        if not api_key.is_valid():
            raise exceptions.AuthenticationFailed('API key expired or inactive')
        
        # Update last_used_at
        api_key.last_used_at = timezone.now()
        api_key.save(update_fields=['last_used_at'])
        
        # Return user (or None if service account)
        return (api_key.user, api_key)
    
    def authenticate_header(self, request):
        return self.keyword