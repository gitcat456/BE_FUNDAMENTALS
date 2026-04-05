import jwt as pyjwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from .models import User
from rest_framework import exceptions

def generate_jwt(user):
    payload = {
        "user_id": user.id,
        "username": user.username,
        "exp":  datetime.now(timezone.utc) + timedelta(hours=1)    
    }
    
    jwt = pyjwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    
    return jwt

def verify_jwt(token):
    
    try:
        payload = pyjwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
        
    except pyjwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed("Token has expired!")
        
    except pyjwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed("Token is invalid!")
        
