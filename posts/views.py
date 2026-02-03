from rest_framework import viewsets
from .models import Author, Posts
from .serializers import AuthorSerializer, PostSerializer
from django.shortcuts import get_object_or_404

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    

class PostViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    
    def get_queryset(self):
        queryset = self.queryset
        search = self.request.query_params.get('search')
        
       
        if search:
            queryset = queryset.filter(title__icontains=search).filter(content__icontains=search)
        return queryset
        
  
        
