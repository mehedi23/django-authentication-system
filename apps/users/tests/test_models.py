# test_models.py	- Fields, methods, __str__
import pytest
from apps.users.models import User
from model_mommy import mommy
from model_bakery import baker

pytestmark = pytest.mark.django_db

def test_user_creation():
    user = User.objects.create_user(username="myid",email="test@example.com",password="TestPassword0123")
    assert user.username == "myid"
    assert user.email == "test@example.com"
    assert user.is_email_verify is False
    assert user.is_phone_verify is False
    assert user.check_password("TestPassword0123") is True

def test_user_str():
    # user = mommy.make(User, username="yoyobro")
    user = baker.make(User, username="yoyobro")
    assert str(user) == user.username 

def test_user_bulk_creation():
    pass 