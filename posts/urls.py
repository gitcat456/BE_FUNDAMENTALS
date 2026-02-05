from django.urls import path, include,re_path
from .views import AuthorViewSet, PostViewSet, post_detail, all_posts
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
#router.register(r'posts', PostViewSet)
router.register(r'author', AuthorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/', all_posts),
    path('posts/<int:id>/', post_detail)
   
    
]
