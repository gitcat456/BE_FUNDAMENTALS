from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from .views import BookViewSet, LoanViewSet, MemberViewSet
from . import views

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'loans', LoanViewSet)
router.register(r'member', MemberViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('list/', views.book_list_view),
    path('create/', views.create_book),
    path('del/<int:pk>/', views.book_delete_view),
    
    #Session auth (Day 1)
    path('auth/register/', views.register_view),
    path('auth/login/', views.login_view),
    path('auth/logout/', views.logout_view),
    path('auth/me/', views.me_view),
    
    # Token auth (Day 2)
    path('auth/token-login/', views.token_login_view),
    path('auth/token-logout/', views.token_logout_view),
    path('auth/token-me/', views.token_me_view),
    
    #jwt auth(Day 5)
    path('auth/jwt-login/', views.jwt_login_view),
    path('auth/jwt-refresh/', views.jwt_refresh_view),
    path('auth/jwt-logout/', views.jwt_logout_view)
]
