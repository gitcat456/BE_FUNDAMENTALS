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
    
    #Nested Serializer or depth=1
    
    
    #slug related field for manyToMany relations..it returns slug names 
    # tags = serializers.SlugRelatedField(
    #         many=True,
    #         read_only=True,
    #         slug_field='name'
    #     )
    #handle write 
    #tags = serializers.SlugRelatedField(
        #     many=True,
        #     queryset=Tag.objects.all(),
        #     slug_field='name'
        # )

    
    #using source..Access nested attributes, rename fields
    tag_count = serializers.IntegerField(source='tags.count', read_only=True)
    author_name = serializers.CharField(source='author.name', read_only=True)
    
    #read only nesting 
    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Posts
        fields = ['id', 'uuid', 'title', 'content', 'author', 'author_name', 'likes', 'tag_count', 'tags']
       
        
       # field level validation 
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must contain more than 5 characters!!")
        
        banned_words = ['fake', 'illegal', 'scam', 'witchcraft']       
        if any(word in value.lower() for word in banned_words):
            raise serializers.ValidationError(
                "Title contains Banned words"
            )
        
        return value 
        
