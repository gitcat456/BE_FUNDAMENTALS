from rest_framework import serializers
from .models import Book, Member, LoanItem, Loan
from django.db import transaction
from django.shortcuts import get_object_or_404

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
         model = Member
         fields = '__all__'

class LoanListSerializer(serializers.ModelSerializer):
    
    member_name = serializers.CharField(source='member.name', read_only=True)
    total_books = serializers.SerializerMethodField()
    
    class Meta:
        model = Loan
        fields = ['id', 'member_name', 'borrowed_date', 'due_date', 'status', 'total_books']
        
    def get_total_books(self, obj):
        return obj.items.count()
    
class LoanItemSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_author = serializers.CharField(source='book.author', read_only=True)
    book_isbn = serializers.CharField(source='book.isbn', read_only=True)
    
    class Meta:
        model = LoanItem
        fields =['book_title', 'book_author', 'book_isbn']

    
class LoanDetailSerializer(LoanListSerializer):
    
    items = LoanItemSerializer(many=True, read_only=True)
    
    class Meta(LoanListSerializer):
        model = Loan
        fields = LoanListSerializer.Meta.fields + ['items']
 
 
@transaction.atomic       
class LoanCreateSerializer(serializers.ModelSerializer):
    
    member_email = serializers.EmailField(write_only=True)
    book_isbns = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )
  
    class Meta:
        model = Loan
        fields = ['member_email', 'due_date', 'book_isbns']
        
    def validate_member_email(self, value):
        if not Member.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user associated with this email!")
        return value
    
    def validate_book_isbns(self, value):
        for isbn in value:
            if not Book.objects.filter(isbn=isbn).exists():
                raise serializers.ValidationError("The book with the isbn entered does not exist!")
            return value
        
    def create(self, validated_data):   #validated_data is just a Python dictionary of cleaned input data.
       email = validated_data.pop('member_email')  #extract these fields form the cleaned input
       isbns = validated_data.pop('book_isbns')
       
    # Get member
       member = Member.objects.get(email=email)
       
       loan = Loan.objects.create(
            member=member,
            **validated_data    #only contains due date right now 
        )
        
       for isbn in isbns:
            book = Book.objects.get(isbn=isbn)

            if book.available_copies < 1:
                raise serializers.ValidationError(
                    f"{book.title} is not available"
                )

            LoanItem.objects.create(
                loan=loan,
                book=book
            )

            book.available_copies -= 1
            book.save()

       return loan
   
    def to_representation(self, instance):
        """Return full order details after creation"""
        return LoanDetailSerializer(instance).data