from django.contrib import admin
from .models import Posts, Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'slug')
    search_fields = ('name', 'email')
   


@admin.register(Posts)
class PostAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'title', 'author',)
    list_filter = ('author', )
    search_fields = ('title', 'content')
    raw_id_fields = ('author',)

