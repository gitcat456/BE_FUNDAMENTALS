import pytest 
from django.test import Client
from ecom.models import Product
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
        
        