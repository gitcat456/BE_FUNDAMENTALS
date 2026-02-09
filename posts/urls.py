from django.urls import path, include,re_path
from .views import AuthorViewSet, PostViewSet, post_detail, all_posts, post_list_create
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'author', AuthorViewSet)

urlpatterns = [
   path('posts/', post_list_create, name = "create_list"),
   path('posts/<int:id>/', post_detail),
   path('posts/<int:id>/edit', post_detail),
   path('posts/<int:id>/delete', post_detail)
   
   #path('', include(router.urls)),
      
]
