import pytest
from decimal import Decimal
from ecom.serializers import OrderListSerializer
from ecom.models import Product, Order, OrderItem

@pytest.mark.django_db
class TestOrderListSerializer:
    """Test computed fields in OrderListSerializer"""
    
    def test_total_price_computed_correctly(self):
        """Test total_price sums all items"""
        # ARRANGE: Create order with items
        product1 = Product.objects.create(
            name="Laptop",
            price=Decimal('100.00'),
            stock=10
        )
        product2 = Product.objects.create(
            name="Mouse",
            price=Decimal('25.00'),
            stock=50
        )
        
        order = Order.objects.create(
            customer_email="test@example.com",
            status="pending"
        )
        
        OrderItem.objects.create(
            order=order,
            product=product1,
            quantity=2,
            price_at_purchase=Decimal('100.00')
        )
        OrderItem.objects.create(
            order=order,
            product=product2,
            quantity=3,
            price_at_purchase=Decimal('25.00')
        )
        
        # ACT: Serialize
        serializer = OrderListSerializer(order)
        
        # ASSERT: total_price = (2 * 100) + (3 * 25) = 275
        assert serializer.data['total_price'] == Decimal('275.00')
    
    def test_total_items_computed(self):
        """Test total_items counts correctly"""
        # ARRANGE
        order = Order.objects.create(
            customer_email="test@example.com",
            status="pending"
        )
        
        product = Product.objects.create(
            name="Laptop",
            price=Decimal('100.00'),
            stock=10
        )
        
        # 2 laptops + 3 mice = 5 total items
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=2,
            price_at_purchase=Decimal('100.00')
        )
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=3,
            price_at_purchase=Decimal('25.00')
        )
        
        # ACT
        serializer = OrderListSerializer(order)
        
        # ASSERT
        assert serializer.data['total_items'] == 5  # 2 + 3