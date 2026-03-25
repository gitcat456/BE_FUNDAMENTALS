import pytest
from posts.models import Author ,Posts

@pytest.mark.django_db
class TestAuthorModel:
    
    def test_create_author(self):
        author = Author.objects.create(
            name = "Lizzy lin",
            email = "lizzy@gmail.com",
            bio = ""
        )
        
        assert author.name == "Lizzy lin"
        assert author.email is not None
        
    def test_author_slug_generated(self):
        
        author2 = Author.objects.create(
            name = "Lucy Kibaki",
            email = "Kibaki@gmail.com"
        )
        
        assert author2.slug == "lucy-kibaki"
        
    def test_email_is_not_none(self):
        
        author3 = Author.objects.create(
            name = "Wangari Miti",
            bio = "I raf",
            email = "wanga@gmail.com"
        )
        
        assert author3.email != ""
        
    def test_author_has_posts(self):
        
        author4 = Author.objects.create(
            name = "Bonie NJuguna",
            email = "BMNFS@gmail.com"
        )
        
        post1 = Posts.objects.create(
            author = author4,
            title = "the trip",
            content = "Coming soon"
        )
        
        post2 = Posts.objects.create(
            author = author4,
            title = "The badGang",
            content = "Coming soon"
        )
        
        assert author4.posts.count() == 2
        
        
        
    