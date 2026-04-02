from django.shortcuts import render
from rest_framework import viewsets
from .models import Book, Loan, Member
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
        
    
    


