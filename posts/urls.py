from django.urls import path, include,re_path
from .views import AuthorViewSet, PostViewSet, post_detail, all_posts, post_list_create, TagViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'author', AuthorViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
   path('posts_list/', post_list_create, name = "create_list"),
   path('posts_fbv/<int:pk>/', post_detail),
   path('posts_fbv/<int:pk>/edit', post_detail),
   path('posts_fbv/<int:pk>/delete', post_detail),
   path('', include(router.urls)),
      
]
