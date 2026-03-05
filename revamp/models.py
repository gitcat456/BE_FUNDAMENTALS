from django.db import models
import uuid

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.name}"
    
class Post(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.title}"
    
class Comment(models.Model):
    content = models.TextField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    likes = models.IntegerField(default=0)
        
    

