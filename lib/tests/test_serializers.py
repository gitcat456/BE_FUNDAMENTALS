import pytest
from datetime import date, timedelta
from lib.serializers import LoanCreateSerializer
from lib.models import Book, Member


@pytest.mark.django_db
class TestLoanCreateSerializer:
    
    def test_valid_loan_data(self):
        
        member = Member.objects.create(
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
        
        serializer = LoanCreateSerializer(data=data)
        assert serializer.is_valid() is True
        assert serializer.errors == {}
        
    def test_empty_books_rejected(self):
        
        member = Member.objects.create(
            name="Kamau Njenga",
            email="km@example.com"
        )
        
        data = {
            "member_email": "km@example.com",
            "due_date": str(date.today() + timedelta(days=14)),
            "book_isbns": []  
        }
        
        serializer = LoanCreateSerializer(data=data)
        assert serializer.is_valid() is False
        assert "book_isbns" in serializer.errors
        
    def  test_invalid_isbn_rejected(self):
        
       member = Member.objects.create(
            name="denly Kibaki",
            email="denly@gmail.com"
        )
       
       data = {
           "member_email": "denly@gmail.com",
           "due_date": str(date.today() + timedelta(days=14)),
           "book_isbns": ["234523", "3453"]
       } 
       
       serializer = LoanCreateSerializer(data=data)
       assert serializer.is_valid() is False
       
    def test_inactive_member_rejected(self):
        
        member = Member.objects.create(
            name="denly Kibaki",
            email="denly@gmail.com",
            membership_active=False
        )
        
        book1 = Book.objects.create(
            title="A man of the people",
            author="Bi Hen",
            isbn=43534345344,
            available_copies=1 
        )
        
        data = {
           "member_email": "denly@gmail.com",
           "due_date": str(date.today() + timedelta(days=14)),
           "book_isbns": [book1.isbn]
        } 
        
        serializer = LoanCreateSerializer(data=data)
        
        assert serializer.is_valid() is True
        
    def test_invalid_email_rejected(self):
        
         member = Member.objects.create(
            name="denly Kibaki",
            email="8943uijsi",
        )
         
         book1 = Book.objects.create(
            title="A man of the people",
            author="Bi Hen",
            isbn=43534345344,
            available_copies=1 
        )
        
         data = {
           "member_email": "8943uijsi",
           "due_date": str(date.today() + timedelta(days=14)),
           "book_isbns": [book1.isbn]
        } 
         
         serializer = LoanCreateSerializer(data=data)
         assert serializer.is_valid() is False
         
    
        
