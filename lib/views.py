from django.shortcuts import render
from rest_framework import viewsets
from .models import Book, Loan, Member
from .serializers import (
    BookSerializer,
    LoanListSerializer,
    LoanDetailSerializer,
    LoanCreateSerializer,
    MemberSerializer
    ) 

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    
class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return LoanListSerializer
        elif self.action == 'retrieve':
            return LoanDetailSerializer
        elif self.action == 'create':
            return LoanCreateSerializer
        return LoanListSerializer
        
    
    


