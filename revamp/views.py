from django.shortcuts import render
from .models import Author, Post, Comment
from .serializers import PostSerializer, AuthorSerializer, CommentSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, action

@api_view(["GET", "POST"])
def createAuthor(request):
    
    if request.method == 'GET':
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": 201,
                "message": "Author created successfully!!",
                "author": request.data     
            }
            
            return Response(response)
        return Response(serializer.errors, status=400)
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        post = self.get_object()
        post.is_published=True
        post.save()
        
        return Response({
            "message": "Post Published successfully"
          
        })
    
    @action(detail=False, methods=['get'])
    def published(self, request):
        posts = Post.objects.filter(is_published=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        post.likes += 1
        post.save()
        
        return Response({
            "message": "Post liked successfully",
            "likes": post.likes
        })
        