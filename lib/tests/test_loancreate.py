import pytest
from lib.models import Book, Loan, Member
from lib.serializers import LoanCreateSerializer
from datetime import date, timedelta

@pytest.mark.django_db
class TestLoanCreateSerializerCreate:
    def test_create_loan_with_books(self):
        
          member = Member.objects.create(
            name="John Doe",
            email="john@example.com"
         )
        
          book1 = Book.objects.create(
            title="Book 1",
            author="Author 1",
            isbn="111",
            available_copies=5
          )
        
          book2 = Book.objects.create(
            title="Book 2",
            author="Author 2",
            isbn="222",
            available_copies=3
          )
        
          data = {
            "member_email": "john@example.com",
            "due_date": str(date.today() + timedelta(days=14)),
            "book_isbns": ["111", "222"]
          }
          
          #ACT
          serializer = LoanCreateSerializer(data=data)
          assert serializer.is_valid() is True
          loan = serializer.save()
          
          #ASSERT
          assert loan is not None
          assert loan.member.email == "john@example.com"
          assert loan.status == "borrowed"
          assert Loan.objects.count() == 1
        
            # ASSERT: Loan items created
          assert loan.items.count() == 2
            
            # ASSERT: Books linked correctly
          loan_books = [item.book for item in loan.items.all()]
          assert book1 in loan_books
          assert book2 in loan_books
            
    def test_create_reduces_available_copies(self):
        
         member = Member.objects.create(
            name="John Doe",
            email="john@example.com"
         )
        
         book = Book.objects.create(
            title="Book 1",
            author="Author 1",
            isbn="111",
            available_copies=5
          )
         
         data = {
            "member_email": "john@example.com",
            "due_date": str(date.today() + timedelta(days=14)),
            "book_isbns": [book.isbn]
         }
         
         serializer = LoanCreateSerializer(data=data)
         assert serializer.is_valid() is True
         loan = serializer.save()
         
         book.refresh_from_db()
         assert book.available_copies == 4