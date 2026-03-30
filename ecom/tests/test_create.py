import pytest 
from ecom.serializers import OrderCreateSerializer
from ecom.models import Product, Order
from decimal import Decimal

@pytest.mark.django_db
class TestOrderCreateSerializerCreate:
    """Test the create() method"""
    
    def test_create_order_with_items(self):
        """Test serializer creates order and items"""
        # ARRANGE
        product1 = Product.objects.create(
            name="Laptop",
            price=Decimal('999.99'),
            stock=10
        )
        product2 = Product.objects.create(
            name="Mouse",
            price=Decimal('25.00'),
            stock=50
        )
        
        data = {
            "customer_email": "test@example.com",
            "items": [
                {"product_id": product1.id, "quantity": 2},
                {"product_id": product2.id, "quantity": 1}
            ]
        }
        
        # ACT: Create the order
        serializer = OrderCreateSerializer(data=data)
        assert serializer.is_valid() is True
        order = serializer.save()
        
        # ASSERT: Order created
        assert order is not None
        assert order.customer_email == "test@example.com"
        assert order.status == "pending"
        assert Order.objects.count() == 1
        
        # ASSERT: Order items created
        assert order.items.count() == 2
        
        # ASSERT: Items have correct data
        items = list(order.items.all())
        assert items[0].product == product1
        assert items[0].quantity == 2
        assert items[0].price_at_purchase == Decimal('999.99')
        
        assert items[1].product == product2
        assert items[1].quantity == 1
        assert items[1].price_at_purchase == Decimal('25.00')
    
    def test_create_reduces_stock(self):
        """Test creating order reduces product stock"""
        # ARRANGE
        product = Product.objects.create(
            name="Laptop",
            price=Decimal('999.99'),
            stock=10
        )
        
        data = {
            "customer_email": "test@example.com",
            "items": [{"product_id": product.id, "quantity": 3}]
        }
        
        # ACT
        serializer = OrderCreateSerializer(data=data)
        serializer.is_valid()
        serializer.save()
        
        # ASSERT: Stock reduced
        product.refresh_from_db()  # Reload from database
        assert product.stock == 7  # 10 - 3 = 7
    
    def test_create_captures_price_at_purchase(self):
        """Test order captures current price, not future changes"""
        # ARRANGE
        product = Product.objects.create(
            name="Laptop",
            price=Decimal('999.99'),
            stock=10
        )
        
        data = {
            "customer_email": "test@example.com",
            "items": [{"product_id": product.id, "quantity": 1}]
        }
        
        # ACT: Create order
        serializer = OrderCreateSerializer(data=data)
        serializer.is_valid()
        order = serializer.save()
        
        # Change product price
        product.price = Decimal('1199.99')
        product.save()
        
        # ASSERT: Order still has old price
        order_item = order.items.first()
        assert order_item.price_at_purchase == Decimal('999.99')
        assert order_item.price_at_purchase != product.price