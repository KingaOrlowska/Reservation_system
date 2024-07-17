import pytest
from django.contrib.auth.models import User
from django.test import Client

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def admin_user():
    return User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')

@pytest.fixture
def reception_user():
    return User.objects.create_user(username='reception', password='reception')
