from rest_framework import serializers
from .models import Author, Posts

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'email','slug' ]

class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())

    class Meta:
        model = Posts
        fields = ['id', 'uuid', 'title', 'content', 'author']
