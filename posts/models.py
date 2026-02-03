import uuid
from django.db import models
from django.utils.text import slugify

#tasks : implement slug and uuid
class Author(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(blank=True, null=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    

class Posts(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=50)
    content = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
