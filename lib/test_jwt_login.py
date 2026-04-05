import pytest
from lib.jwt_utils import generate_jwt, verify_jwt
from lib.models import User
from rest_framework import exceptions

@pytest.mark.django_db
def test_generate_jwt():
    user = User.objects.create_user(
        username = "testDen",
        email = "test@example.com",
        password = "secpass123",
        phone = "+254 723 234 234"
    )
    
    jwt = generate_jwt(user)
    
    assert isinstance(jwt, str)
    parts = jwt.split(".")
    assert len(parts) ==3

@pytest.mark.django_db
def test_verify_valid_jwt():
    
    user = User.objects.create_user(
        username = "testDen",
        email = "test@example.com",
        password = "secpass123",
        phone = "+254 723 234 234"
    )
    
    jwt = generate_jwt(user)
    payload =verify_jwt(jwt)  # returns decoded payload dict
    
    # ssert payload contains user_id
    assert "user_id" in payload, "Payload missing user_id"

    #Fetch user from payload
    user_from_token = User.objects.get(id=payload["user_id"])

    # Assert returned user matches original
    assert user_from_token == user, "JWT user does not match original"
    

@pytest.mark.django_db
def test_verify_invalid_jwt():
    # jwt = "kjbsifiuh89834.4935y3948934gtujs.&t989Ubijvnwehfwo"
    
    # response = verify_jwt(jwt)
    
    pass
    

    
    