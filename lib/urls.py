from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from .views import BookViewSet, LoanViewSet, MemberViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'loans', LoanViewSet)
router.register(r'member', MemberViewSet)

urlpatterns = [
    path('', include(router.urls))
]