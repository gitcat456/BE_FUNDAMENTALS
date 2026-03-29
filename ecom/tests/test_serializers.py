import pytest
from decimal import Decimal
from ecom.serializers import OrderCreateSerializer
from ecom.models import Product, Order

@pytest.mark.django_db
class TestOrderCreateSerializer:
    """Test OrderCreateSerializer validation"""
    
    def test_valid_order_data(self):
        """Test serializer accepts valid data"""
        product = Product.objects.create(
            name="Laptop",
            price=Decimal('999.99'),
            stock=10
        )
        
        data = {
            "customer_email": "test@example.com",
            "items": [{"product_id": product.id, "quantity": 2}]
        }
        
        serializer = OrderCreateSerializer(data=data)
        assert serializer.is_valid() is True
    
    def test_empty_items_rejected(self):
        """Test serializer rejects empty items"""
        data = {
            "customer_email": "test@example.com",
            "items": []
        }
        
        serializer = OrderCreateSerializer(data=data)
        assert serializer.is_valid() is False
        assert "items" in serializer.errors
    
    def test_invalid_email_rejected(self):
        """Test invalid email format rejected"""
        data = {
            "customer_email": "ks_Lmewfn",
            "items": [{"product_id": 1, "quantity": 1}]
        }
        
        serializer = OrderCreateSerializer(data=data)
        assert serializer.is_valid() is False
        assert "customer_email" in serializer.errors
    
    def test_missing_required_fields(self):
        """Test missing required fields"""
        data = {}  # No fields
        
        serializer = OrderCreateSerializer(data=data)
        assert serializer.is_valid() is False
        assert "customer_email" in serializer.errors
        assert "items" in serializer.errors
    
    def test_create_order_success(self):
        """Test serializer creates order correctly"""
        product = Product.objects.create(
            name="Laptop",
            price=Decimal('999.99'),
            stock=10
        )
        
        data = {
            "customer_email": "test@example.com",
            "items": [{"product_id": product.id, "quantity": 2}]
        }
        
        serializer = OrderCreateSerializer(data=data)
        assert serializer.is_valid() is True
        
        # ACT: Create the order
        order = serializer.save()
        
        # ASSERT: Order created correctly
        assert order.customer_email == "test@example.com"
        assert order.items.count() == 1
        
        # ASSERT: OrderItem created correctly
        order_item = order.items.first()
        assert order_item.product == product
        assert order_item.quantity == 2
        assert order_item.price_at_purchase == product.price
        
        # ASSERT: Stock reduced
        product.refresh_from_db()
        assert product.stock == 8  # 10 - 2