from rest_framework import serializers
from .models import Author, Posts, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'email','slug' ]

class PostSerializer(serializers.ModelSerializer):
    
    # PrimaryKeyRelatedField (for write support)
    # tags = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=Tag.objects.all()
    # )

    # author = serializers.PrimaryKeyRelatedField(
    #     queryset=Author.objects.all()
    # )
    
    #Nested Serializer
    #tags = TagSerializer(many=True, read_only=True)
    
    #slug related field for manyToMany relations
    #tags = serializers.SlugRelatedField(
        #     many=True,
        #     read_only=True,
        #     slug_field='name'
        # )
    
    #using source
    tag_count = serializers.IntegerField(source='tags.count', read_only=True)
    

    
    class Meta:
        model = Posts
        fields = ['id', 'uuid', 'title', 'content', 'author', 'tag_count', 'tags']
        
    
        
