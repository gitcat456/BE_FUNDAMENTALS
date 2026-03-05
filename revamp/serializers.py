from rest_framework import serializers
from .models import Author, Post, Comment 
import time

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        
class PostSerializer(serializers.ModelSerializer):
    last_opened = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'uuid', 'author', 'title', 'content', 'is_published', 'likes', 'last_opened']
        read_only_fields = ['uuid', 'is_published']
        
    def get_last_opened(self, obj):
        return time.time()
        
class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ['author', 'post', 'content']