from django.shortcuts import render
from rest_framework import viewsets
from .models import Book, Loan, Member
from rest_framework import exceptions
from .serializers import (
    BookSerializer,
    LoanListSerializer,
    LoanDetailSerializer,
    LoanCreateSerializer,
    MemberSerializer ) 

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from json.decoder import JSONDecodeError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import User


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import AuthToken
from .authentication import TokenAuthentication
from .jwt_utils import generate_jwt
from .refresh_utils import create_refresh_token
from .refresh_utils import rotate_refresh_token
from .refresh_utils import revoke_all_user_tokens
from .permissions import IsLibrarian, IsAdminOrReadOnly 


#jwt login view
@api_view(['POST'])
@permission_classes([AllowAny])
def jwt_login_view(request):
    
    if not request.body or request.body == {}:
        return Response({
            "message": "Request body cannot be empty"
        }, status = 400)
        
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Username and password required'
        }, status=400)
        
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response({
            "message": "Invalid credentials"
        }, status=400)
    
    access_token = generate_jwt(user)
    refresh_token = create_refresh_token(user)
        
    return Response({
        "accessToken": access_token,
        "refreshToken": refresh_token.token
    },status=200)
    
    


@api_view(['POST'])
@permission_classes([AllowAny])
def jwt_refresh_view(request):
    """
    Refresh access token using refresh token
    
    POST /api/auth/jwt-refresh/
    {
        "refresh": "a1b2c3d4..."
    }
    
    Response:
    {
        "access": "eyJhbG...",  // NEW access token
        "refresh": "e5f6g7..."  // NEW refresh token (rotation)
    }
    """
    refresh_token_string = request.data.get('refresh')
    
    if not refresh_token_string:
        raise exceptions.AuthenticationFailed("Refresh Token Not Found!")
        
    
    try:
        # TODO: Rotate refresh token (invalidate old, get new)
        new_refresh_token = rotate_refresh_token(refresh_token_string)
        
        # TODO: Generate new access token for the user
        new_access_token = generate_jwt(new_refresh_token.user)
        
        # TODO: Return both new tokens
        return Response({
            'access': new_access_token,
            'refresh': new_refresh_token.token
        }, status=200)
        
    except exceptions.AuthenticationFailed as e:
        return Response({
            'error': str(e)
        }, status=401)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def jwt_logout_view(request):
    """
    Logout by revoking all refresh tokens
    
    Requires: Authorization: Bearer <access_token>
    
    POST /api/auth/jwt-logout/
    
    Response:
    {
        "message": "Logged out from all devices"
    }
    """
    # TODO: Revoke all refresh tokens for current user
    revoke_all_user_tokens(request.user)
    
    return Response({
        'message': 'Logged out from all devices'
    }, status=200)

@api_view(['POST'])
@permission_classes([AllowAny])
def token_login_view(request):
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Username and password required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Authenticate user
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Get or create token
    token, created = AuthToken.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def token_logout_view(request):
    """
    Logout by deleting token
    
    Requires: Authorization: Token abc123
    """
    # Delete user's token
    try:
        request.user.auth_token.delete()
    except AuthToken.DoesNotExist:
        pass
    
    return Response({
        'message': 'Logged out successfully'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def token_me_view(request):
    """
    Get current user info
    
    Requires: Authorization: Token abc123
    """
    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email
    })


#Sessions authentication
@csrf_exempt
@require_http_methods(["POST"])
def register_view(request):
    """Register a new user"""
    
    if not request.body:
        return JsonResponse({
            'error': 'Request body is empty!'
        }, status=400)
        
    # Handle invalid JSON
    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return JsonResponse(
            {'error': 'Invalid JSON format'}, 
            status=400
        )
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Validation
    if not username or not email or not password:
        return JsonResponse({
            'error': 'Username, email, and password required'
        }, status=400)
    
    # Check if user exists
    if User.objects.filter(username=username).exists():
        return JsonResponse({
            'error': 'Username already exists'
        }, status=400)
    
    # Create user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password  # Django hashes this automatically!
    )
    
    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'email': user.email
    }, status=201)


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    
    if not request.body:
        return JsonResponse({
            'error': 'the request body is empty!'
        }, status=400)
    
    """Login user with session"""
    data = json.loads(request.body)
    
    username = data.get('username')
    password = data.get('password')
    
    # Authenticate
    user = authenticate(request, username=username, password=password)
    
    if user is None:
        return JsonResponse({
            'error': 'Invalid credentials'
        }, status=401)
    
    # Create session in the db for an authenticated user 
    login(request, user)
    
    # Get session ID from the cookie that was just set
    session_id = request.session.session_key
    
    return JsonResponse({
        'message': 'Login successful',
        'session_id': session_id,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    })

@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    """Destroy the user session"""
    logout(request)
    return JsonResponse({'message': 'Logged out'})


@require_http_methods(["GET"])
def me_view(request):
    """Get current user info"""
    if not request.user.is_authenticated:
        return JsonResponse({
            'error': 'Not authenticated'
        }, status=401)
    
    return JsonResponse({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email
    })
    
@permission_classes([IsAuthenticated])
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    
class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return LoanListSerializer
        elif self.action == 'retrieve':
            return LoanDetailSerializer
        elif self.action == 'create':
            return LoanCreateSerializer
        return LoanListSerializer
    
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def book_list_view(request):
    books = Book.objects.all()    
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsLibrarian])
def create_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
       
    
        
    
    


