import pytest 
from django.test import Client
from ecom.models import Product, Order
from decimal import Decimal

@pytest.mark.django_db
class TestProductListView:
       def test_list_products_success(self):
           
        """Test listing products returns 200"""
        
        Product.objects.create(
            name="Laptop",
            price=Decimal('999.99'),
            stock=10
        )
        Product.objects.create(
            name="Mouse",
            price=Decimal('25.00'),
            stock=50
        )
        
        client = Client()
        response = client.get('/api/products/')
        
        #Assert: status code 
        assert response.status_code == 200
        
        #Assert: Response contains product 
        
        data = response.json()
        print(data)
        
        assert len(data) == 2
        assert data[0]['name'] == "Laptop"
        assert data[1]['stock'] == 50
        
        
        
@pytest.mark.django_db
class TestOrderCreateView:
    
    def test_create_order_success(self):
        """Test creating order with valid data return 201"""
        
        prod = Product.objects.create(
            name="Mouse",
            price=Decimal('25.00'),
            stock=50
        )
        
        data = {
            "customer_email": "test@example.com",
            "items": [{"product_id": prod.id, "quantity": 2}]
        }
        
        client = Client()
        response = client.post('/api/order_create/', data=data, content_type = "application/json")
        
        assert response.status_code == 201
        # ASSERT: Order created in database
        assert Order.objects.count() == 1
        
    def test_order_create_invalid_data(self):
        
        prod = Product.objects.create(
            name="Mouse",
            price=Decimal('25.00'),
            stock=50
        )
        
        data = {
            "customer_email": "test@example.com",
            "items": []
        }
        
        client = Client()
        response = client.post('/api/order_create/', data=data, content_type="application/json")
        
        assert response.status_code == 400
        assert Order.objects.count() == 0
        assert "items" in response.json()
     
    def test_create_order_missing_fields(self):
        
        prod = Product.objects.create(
            name="Mouse",
            price=Decimal('25.00'),
            stock=50
        )
        
        data = {
            "items": [{"product_id": prod.id, "quantity": 2}]
        }
        
        client = Client()
        response = client.post('/api/order_create/', data=data, content_type="application/json")
        
        data = response.json()
        
        assert "customer_email" in data
 
@pytest.mark.django_db       
class TestOrderDetailView:
    
    """Test GET /api/orders/{id}/"""
    def test_get_order_success(self):
        
        order = Order.objects.create(
            customer_email="test@example.com",
            status="pending"
        )
        
        client = Client()
        response = client.get(f'/api/orders/{order.id}/')
        
        assert response.status_code == 200
        assert response.json()['id'] == order.id
        assert response.json()['customer_email'] == "test@example.com"
        
    def test_order_not_found(self):
        
        client = Client()
        response = client.get('/api/orders/999/')
        
        assert response.status_code == 404