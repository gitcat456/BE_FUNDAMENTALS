from django.urls import path, include
from .views import createAuthor, PostViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'rvmp/posts', PostViewSet)

urlpatterns = [
    path('rvmp/author_create/',createAuthor, name='author_create'),
    path('', include(router.urls)),
]