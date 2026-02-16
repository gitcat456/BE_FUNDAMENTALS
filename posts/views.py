from rest_framework import viewsets
from .models import Author, Posts, Tag
from .serializers import AuthorSerializer, PostSerializer, TagSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime
from django.utils import timezone

@api_view(["GET", "POST"])
def post_list_create(request):
    
    if request.method == "GET":
        posts = Posts.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        print(request.data)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            response = {
                "status":201,
                "message":"post created successfully",
                "post":{
                        "uuid": serializer.data["uuid"],
                        "title": serializer.data["title"]
                    }
            }
            
            return Response(response)
        return Response(serializer.errors, status=400)
       

@api_view(["GET","PATCH", "DELETE"])
def post_detail(request, pk):
    
    post = get_object_or_404(Posts, pk=pk)
    
    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    elif request.method == "PATCH":
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response= {
                "updated by": "user3435",
                "status": 200,
                "message": "post updated successfully",
                "post" : serializer.data,
                "updated at": timezone.now()
            }
            return Response(response)
        return Response(serializer.errors, status=400)
    
    elif request.method == "DELETE":
        post.delete()
        return Response(status=204)
        
    
    
    
    
    
    
    

def post_details(request, id):
        post = get_object_or_404(Posts, id=id)
        res = {
            "title": post.title,
            "uuid": post.uuid
        }
        return JsonResponse(res)
    

def all_posts(request, safe=False):
    posts = list(Posts.objects.values())
    return JsonResponse(posts, safe=False)
    
# @method_decorator(login_required, name="dispatch")
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
        
  
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
        
