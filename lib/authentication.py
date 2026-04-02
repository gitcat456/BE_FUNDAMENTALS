from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import authentication, exceptions
from .models import AuthToken

User = get_user_model()


class TokenAuthentication(authentication.BaseAuthentication):
    """
    Custom token authentication
    
    Clients should authenticate by passing the token in the "Authorization"
    HTTP header, prepended with the string "Token ".
    
    Example:
        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """
    
    keyword = 'Token'
    
    def authenticate(self, request):
        """
        Returns a User if a valid token is provided, otherwise None
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header:
            return None
        
        # Check if header starts with "Token "
        parts = auth_header.split()
        
        if len(parts) != 2:
            raise exceptions.AuthenticationFailed(_('Invalid token header'))
        
        if parts[0] != self.keyword:
            return None
        
        token_key = parts[1]
        
        return self.authenticate_credentials(token_key)
    
    def authenticate_credentials(self, key):
        """
        Validate token and return user
        """
        try:
            token = AuthToken.objects.select_related('user').get(key=key)
        except AuthToken.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token'))
        
        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted'))
        
        return (token.user, token)
    
    def authenticate_header(self, request):
        """
        Return string to be used as WWW-Authenticate header
        """
        return self.keyword