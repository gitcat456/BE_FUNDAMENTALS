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
from lib.services.email_service import send_order_confirmation_email

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
        order = serializer.save()
        
        # fire confirmation email after order is created
        try:
            send_order_confirmation_email(order)
        except Exception as e:
            # don't fail the order if email fails
            print(f"Email failed: {e}")
        
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
    
    def perform_create(self, serializer):
        order = serializer.save()
        try:
            send_order_confirmation_email(order)
        except Exception as e:
            print(f"Email failed: {e}")
            

from lib.services.cloudinary_service import upload_product_image, upload_order_attachment

ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp']


@api_view(['POST'])
def upload_product_image_view(request, product_id):
    """POST /api/products/<id>/image/"""
    if 'image' not in request.FILES:
        return Response({'error': 'No image provided'}, status=400)

    file = request.FILES['image']

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        return Response({'error': 'Only JPEG, PNG, WEBP allowed'}, status=400)

    if file.size > 5 * 1024 * 1024:
        return Response({'error': 'Max file size is 5MB'}, status=400)

    try:
        product = Product.objects.get(id=product_id)
        url = upload_product_image(file, product_id)
        product.image_url = url
        product.save()
        return Response({'image_url': url})
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
def upload_order_attachment_view(request, order_id):
    """POST /api/orders/<id>/attachment/"""
    if 'attachment' not in request.FILES:
        return Response({'error': 'No file provided'}, status=400)

    file = request.FILES['attachment']

    if file.size > 10 * 1024 * 1024:
        return Response({'error': 'Max file size is 10MB'}, status=400)

    try:
        order = Order.objects.get(id=order_id)
        url = upload_order_attachment(file, order_id)
        order_item = order.items.first()
        if order_item:
            order_item.attachment_url = url
            order_item.save()
        return Response({'attachment_url': url})
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)