import pytest
from decimal import Decimal
from lib.models import Book
from django.test import Client

@pytest.mark.django_db
class TestBookListView:
    
    """ Test listing products returns 200 """
    def test_list_books_success(self):
        
        Book.objects.create(
            title = "Found Her",
            author = "Bien kasik",
            isbn = "9823y4o3592",
            available_copies = 50
        )
        Book.objects.create(
            title = "The end",
            author = "Kenkobin",
            isbn = "3653446gfe",
            available_copies = 32
        )
        
        client = Client()
        response = client.get('/api/books/')
        assert response.status_code == 200
        
        data = response.json()
        assert data[0]['author'] == "Bien kasik"
        
        

