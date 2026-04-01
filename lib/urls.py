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
    path('auth/register/', views.register_view),
    path('auth/login/', views.login_view),
    path('auth/logout/', views.logout_view),
    path('auth/me/', views.me_view),
]