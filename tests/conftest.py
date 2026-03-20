import pytest
import django
from django.test import Client


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def api_base_url():
    return "http://localhost:8001"
