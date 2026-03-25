import pytest 
from ecom.models import Product , Order, OrderItem

@pytest.mark.django_db
def test_create_product():
    
    product = Product.objects.create(
        name="laptop",
        price=99999.90,
        stock=10        
    ) 
    assert product.name == "laptop"
    assert product.stock ==10


@pytest.mark.django_db
def test_order_can_have_multiple_items():
    """Test that an order can have multiple items"""
    
    # ARRANGE: Create products and order
    product1 = Product.objects.create(name="Laptop", price=999.99, stock=10)
    product2 = Product.objects.create(name="Mouse", price=25.00, stock=50)
    
    order = Order.objects.create(
        customer_email="test@example.com",
        status="pending"
    )
    
    # ACT: Add items to order
    OrderItem.objects.create(
        order=order,
        product=product1,
        quantity=1,
        price_at_purchase=999.99
    )
    OrderItem.objects.create(
        order=order,
        product=product2,
        quantity=2,
        price_at_purchase=25.00
    )
    
    # ASSERT: Check order has 2 items
    assert order.items.count() == 2
    
    # ASSERT: Check the items are correct
    items = list(order.items.all())
    assert items[0].product == product1
    assert items[1].product == product2
    
    

@pytest.mark.django_db
class TestProductModel:
    """All tests for Product model"""
    
    def test_create_product(self):
        """Test creating a product"""
        product = Product.objects.create(
            name="Laptop",
            price=999.99,
            stock=10
        )
        assert product.name == "Laptop"
    
    def test_product_price_is_positive(self):
        """Test product price must be positive"""
        product = Product.objects.create(
            name="Laptop",
            price=999.99,
            stock=10
        )
        assert product.price > 0
    
    def test_product_has_stock(self):
        """Test product stock tracking"""
        product = Product.objects.create(
            name="Laptop",
            price=999.99,
            stock=5
        )
        assert product.stock == 5