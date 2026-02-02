from django.db import models

#tasks : implement slug and uuid
class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(min_lenght=2, max_lenght=50)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    

class Posts(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_lenght=50)
    content = models.TextField()
    date_published = models.DateTimeField(auto_add_now=True)
    
