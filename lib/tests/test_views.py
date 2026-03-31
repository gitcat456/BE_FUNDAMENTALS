import pytest
from datetime import date, timedelta
from lib.models import Book, Member, Loan
from django.test import Client

@pytest.mark.django_db
class TestLoanCreateView:
    
    def test_loan_create_success(self):
        
        Member.objects.create(
             name="Tester",
            email="tester@gmail.com"
        )
        
        book1 = Book.objects.create(
            title="A man of the people",
            author="Bi Hen",
            isbn=43534345344,
            available_copies=1 
        )
        
        data = {
            "member_email": "tester@gmail.com",
            "book_isbns": [book1.isbn],
            "due_date": str(date.today() + timedelta(days=14)),
        }
        
        client = Client()
        response = client.post('/api/loans/', data=data, content_type="application/json")
        
        assert response.status_code == 201
        assert Loan.objects.count() == 1
        
    def test_order_create_invalid_data(self):
         
         book1 = Book.objects.create(
            title="A man of the people",
            author="Bi Hen",
            isbn=43534345344,
            available_copies=1 
        )
        
         data = {
            "member_email": "tester@gmail.com",
            "book_isbns": [book1.isbn],
            "due_date": str(date.today() + timedelta(days=14)),
        }
        
         client = Client()
         response = client.post('/api/loans/', data=data, content_type="application/json")
        
         assert response.status_code == 400
         assert "member_email" in response.json()
         
        
     
     