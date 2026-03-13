from django.shortcuts import render
from .models import Order, OrderItem, Product
from .serializers import (
    OrderListSerializer,
    OrderDetailSerializer,
    OrderCreateSerializer,
    ProductSerializer,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404

class ProductViewset(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    
@api_view(["GET"])
def order_list(request):
    order = Order.objects.all()
    serializers = OrderListSerializer(order, many=True)
    return Response(serializers.data)


@api_view(["POST"])
def order_create(request):
    
    serializer =  OrderCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(["GET"])
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    serializer = OrderDetailSerializer(order)
    return Response(serializer.data)


  
#the simplest and smart way ##
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        elif self.action == 'retrieve':
            return OrderDetailSerializer
        elif self.action == 'create':
            return OrderCreateSerializer
        return OrderListSerializer