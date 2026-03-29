import pytest 
from datetime import date, timedelta
from lib.models import Book, Member, Loan, LoanItem



@pytest.mark.django_db
class TestLibraryModels:
    def test_create_book(self):
        
        book1 = Book.objects.create(
            title="A man of the people",
            author="Bi Hen",
            isbn=43534345344,
            available_copies=1 
        )
        
        assert book1.author == "Bi Hen"
        
    def test_member_can_borrow_book(self):
        
        book1 = Book.objects.create(
            title="A man of the people",
            author="Bi Hen",
            isbn=43534345344,
            available_copies=1 
        )
        
        memberOne = Member.objects.create(
            name="Kamau Njenga",
            email="km@example.com"
        )
        
        loan = Loan.objects.create(
            member = memberOne,
            due_date = str(date.today() + timedelta(days=14)),
        )
        
        litem = LoanItem.objects.create(
            loan = loan,
            book = book1
        )
        
        assert loan.items.count() == 1
        
        
    