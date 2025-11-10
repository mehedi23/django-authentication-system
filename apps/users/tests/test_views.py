# test_views.py	Response status, content, templates
from apps.users.models import User
from rest_framework.test import APIClient
from model_mommy import mommy 
import pytest

pytestmark = pytest.mark.django_db

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username="bro",email="bro@example.com",password="broPassword123")

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

# ------------------------------
# UserView tests
# ------------------------------
def test_get_user(auth_client, user):
    pass 

def test_put_user(auth_client, user):
    pass 

def test_patch_user(auth_client, user):
    pass 


def test_delete_user(auth_client, user):
    pass 

def test_post_user_not_allowed_with_empty_data(auth_client):
    pass 

# ------------------------------
# ChangePasswordView tests
# ------------------------------
def test_change_password(auth_client, user):
    pass 

