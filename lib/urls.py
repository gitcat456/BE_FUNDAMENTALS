from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from .views import BookViewSet, LoanViewSet
from . import views

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'loans', LoanViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('list/', views.book_list_view),
    path('create/', views.create_book),
    path('del/<int:pk>/', views.book_delete_view),
    path('loan-list/', views.loan_list_view),
    
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
    path('auth/jwt-logout/', views.jwt_logout_view),
    path('auth/profile/', views.profile_view),
    
    #apikeys
    path('api-keys/create/', views.create_api_key_view),
    path('api-keys/', views.list_api_keys_view),
    path('api-keys/<int:key_id>/revoke/', views.revoke_api_key_view),
    
    #security
    path('search/', views.vulnerable_search),
    
    #password resets
    path('auth/forgot-password/', views.forgot_password),
    path('auth/reset-password/', views.reset_password),
    
    # profile
    path('users/profile/', views.get_profile),
    path('users/profile/update/', views.update_profile),
    path('users/profile/photo/', views.upload_profile_photo_view),
    
     # maps
    path('maps/geocode/', views.geocode_view),
    path('maps/reverse-geocode/', views.reverse_geocode_view),
    path('maps/nearby-users/', views.nearby_users_view),
    path('maps/distance/<int:user_id>/', views.distance_between_users),
]
