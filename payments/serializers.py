# payments/serializers.py
from rest_framework import serializers
from .models import Payment
from lib.models import Loan, LoanItem, Book
from datetime import date, timedelta


class BookBorrowItemSerializer(serializers.Serializer):
    """
    Input: list of book IDs member wants to borrow
    [{"book_id": 1}, {"book_id": 3}]
    """
    book_id = serializers.IntegerField()

    def validate_book_id(self, value):
        try:
            book = Book.objects.get(id=value)
        except Book.DoesNotExist:
            raise serializers.ValidationError(f"Book {value} does not exist")

        if book.available_copies < 1:
            raise serializers.ValidationError(
                f"'{book.title}' has no available copies"
            )
        return value


class LoanRequestSerializer(serializers.Serializer):
    """
    Full loan request input validator.
    Member sends: { "books": [{"book_id": 1}, {"book_id": 2}] }
    """
    books = serializers.ListField(
        child=BookBorrowItemSerializer(),
        min_length=1,
        max_length=5   # max 5 books per loan — business rule
    )

    def validate_books(self, value):
        # check for duplicate book IDs
        book_ids = [item['book_id'] for item in value]
        if len(book_ids) != len(set(book_ids)):
            raise serializers.ValidationError("Duplicate books in request")
        return value


class PaymentSerializer(serializers.ModelSerializer):
    """Read-only payment details returned to frontend"""
    loan_id = serializers.IntegerField(source='loan.id', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'reference', 'expected_amount',
            'amount_paid', 'status', 'loan_id',
            'created_at', 'paid_at'
        ]
        read_only_fields = fields