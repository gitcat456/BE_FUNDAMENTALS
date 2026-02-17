from rest_framework import serializers
from .models import Author, Posts, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'email','slug' ]

class PostSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    author = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all()
    )
    
    class Meta:
        model = Posts
        fields = ['id', 'uuid', 'title', 'content', 'author', 'tags']
        
    
        
