# tests/conftest.py
import pytest
from django.contrib.auth import get_user_model

@pytest.fixture
def user_factory(db):
    """A factory to create user instances."""
    def create_user(**kwargs):
        User = get_user_model()
        return User.objects.create_user(**kwargs)
    return create_user