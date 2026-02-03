from django.urls import path, include,re_path
from .views import AuthorViewSet, PostViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'author', AuthorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
]
