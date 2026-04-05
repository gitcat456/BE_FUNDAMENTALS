from rest_framework import authentication, exceptions
from .jwt_utils import verify_jwt
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTAuthentication(authentication.BaseAuthentication):
    keyword = 'Bearer'
    
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None 

        if not auth_header.startswith(f'{self.keyword} '):
            return None 

        #Extract token
        token = auth_header[len(self.keyword)+1:]  # skip "Bearer "

        #Verify JWT
        try:
            payload = verify_jwt(token)  # should return decoded data
        except Exception as e:
            raise exceptions.AuthenticationFailed('Invalid or expired token') from e

        #Get user from payload
        try:
            user_id = payload.get('user_id') 
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        #Return user and None
        return (user, None)