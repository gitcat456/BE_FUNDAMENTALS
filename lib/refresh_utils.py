from datetime import datetime, timedelta, timezone
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from .models import RefreshToken


User = get_user_model() 


def create_refresh_token(user):
    
    """
    Create a new refresh token for user 
    Returns:
        RefreshToken object
    """
    #TODO: generate Token
    token = RefreshToken.generate_token()
    
    #TODO: set expiry time
    expires_at =  datetime.now(timezone.utc) + timedelta(days=7)
    
    refresh_token = RefreshToken.objects.create(
        user=user,
        token=token, 
        expires_at=expires_at
        )
    
    return refresh_token


def verify_refresh_token(token_string):
    """
    Verify refresh token and return user
    
    Args:
        token_string: The refresh token string
    
    Returns:
        User object if valid
    
    Raises:
        AuthenticationFailed if invalid/expired/revoked
    """
    try:
        # TODO: Look up token in database
        token = RefreshToken.objects.get(token=token_string)
    except RefreshToken.DoesNotExist:
       raise exceptions.AuthenticationFailed("Refresh token does not exist!")
        
    
    # TODO: Check if token is valid (not expired, not revoked)
    if not token.is_valid():
        raise exceptions.AuthenticationFailed("Refresh Token in invalid,expired or revoked!!")
        
    
    # TODO: Return user
    return token.user


def rotate_refresh_token(old_token_string):
    """
    Rotate refresh token (invalidate old, create new)
    
    This is the TOKEN ROTATION security feature.
    
    Args:
        old_token_string: The old refresh token
    
    Returns:
        New RefreshToken object
    
    Raises:
        AuthenticationFailed if old token invalid
    """
    # TODO: Get old token from database
    try:
        old_token = RefreshToken.objects.get(token=old_token_string)
    except RefreshToken.DoesNotExist:
        raise exceptions.AuthenticationFailed("RefreshToken does not exist!")
    
    # TODO: Check if old token is valid
    if not old_token.is_valid():
        raise exceptions.AuthenticationFailed("RefreshToken is Invalid!")
    
    # TODO: Mark old token as revoked
    old_token.revoked = True
    old_token.save()
    
    # TODO: Create new refresh token for same user
    new_token = create_refresh_token(old_token.user)
    
    return new_token


def revoke_all_user_tokens(user):
    """
    Revoke all refresh tokens for a user
    
    Use this when:
    - User changes password
    - Security breach detected
    - User logs out from all devices
    """
    
    tokens = user.refresh_tokens.filter(revoked=False)
    tokens.update(revoked=True)  # Just set revoked=True
