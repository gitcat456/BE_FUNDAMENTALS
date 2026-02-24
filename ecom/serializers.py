from rest_framework import serializers
from .models import Product, OrderItem, Order
from django.db import transaction

class OrderListSerializer(serializers.ModelSerializer):
    total_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'customer_email', 'status', 'total_items', 'total_price', 'created_at']
    
    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())
    
    def get_total_price(self, obj):
        total = 0
        for item in obj.items.all():
            total += item.quantity * item.price_at_purchase
        return total


class OrderItemDetailSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['product_name', 'quantity', 'price_at_purchase', 'subtotal']
    
    def get_subtotal(self, obj):
        return obj.quantity * obj.price_at_purchase


class OrderDetailSerializer(OrderListSerializer):
    items = OrderItemDetailSerializer(many=True, read_only=True)
    
    class Meta(OrderListSerializer.Meta):
        fields = OrderListSerializer.Meta.fields + ['items']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = serializers.ListField(
        child=serializers.DictField(),
        write_only=True
    )
    
    class Meta:
        model = Order
        fields = ['customer_email', 'items']
    
    def validate_items(self, value):
        """Validate the items list"""
        # Check items list is not empty
        if not value:
            raise serializers.ValidationError("Order must contain at least one item")
        
        # Check each item structure
        for item in value:
            if 'product_id' not in item:
                raise serializers.ValidationError("Each item must have a product_id")
            if 'quantity' not in item:
                raise serializers.ValidationError("Each item must have a quantity")
            
            # Check quantity is positive
            try:
                quantity = int(item['quantity'])
                if quantity <= 0:
                    raise serializers.ValidationError("Quantity must be greater than 0")
            except (ValueError, TypeError):
                raise serializers.ValidationError("Quantity must be a valid number")
        
        # Check for duplicate products
        product_ids = [item['product_id'] for item in value]
        if len(product_ids) != len(set(product_ids)):
            duplicates = [pid for pid in product_ids if product_ids.count(pid) > 1]
            raise serializers.ValidationError(
                f"Duplicate products in order. Product {duplicates[0]} appears multiple times"
            )
        
        return value
    
    def validate(self, data):
        """Validate products exist and have sufficient stock"""
        items = data.get('items', [])
        
        for item in items:
            product_id = item['product_id']
            quantity = item['quantity']
            
            # Check product exists
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError({
                    'items': f"Product with id {product_id} does not exist"
                })
            
            # Check sufficient stock
            if product.stock < quantity:
                raise serializers.ValidationError({
                    'items': f"Only {product.stock} units of {product.name} available"
                })
        
        return data
    
    @transaction.atomic  # This ensures all DB operations succeed or all fail
    def create(self, validated_data):
        """Create order and order items"""
        # Extract items data
        items_data = validated_data.pop('items')
        
        # Create the order
        order = Order.objects.create(
            customer_email=validated_data['customer_email'],
            status='pending'
        )
        
        # Create order items and update stock
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])
            
            # Create order item
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price_at_purchase=product.price  # Capture current price
            )
            
            # Reduce stock
            product.stock -= item_data['quantity']
            product.save()
        
        return order
    
    def to_representation(self, instance):
        """Return full order details after creation"""
        return OrderDetailSerializer(instance).data