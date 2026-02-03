from rest_framework import viewsets
from .models import Author, Posts
from .serializers import AuthorSerializer, PostSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse

def post_detail(request, id):
    if request.method != "GET":
        post = Posts.objects.get(id=id)
        res = {
            "title": post.title,
            "uuid": post.uuid
        }
        return JsonResponse(res)
    else :
       print('Method is a GET request')
    
    return HttpResponse("Cha He KaFei!")
    

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
            queryset = queryset.filter(title__icontains=search)
        return queryset
        
  
        
