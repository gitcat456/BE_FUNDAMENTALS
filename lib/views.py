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
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import User

@csrf_exempt
@require_http_methods(["POST"])
def register_view(request):
    """Register a new user"""
    data = json.loads(request.body)
    
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
    
    return JsonResponse({
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    })


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
        
    
    


