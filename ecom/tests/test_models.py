import pytest 
from ecom.models import Product 

@pytest.mark.django_db
def test_create_product():
    
    product = Product.objects.create(
        name="laptop",
        price=99999.90,
        stock=10        
    )
    
    
    assert product.name == "laptop"
    assert product.stock ==10