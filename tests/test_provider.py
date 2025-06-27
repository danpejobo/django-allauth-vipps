# tests/test_provider.py
import pytest
from vipps_auth.provider import VippsProvider
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

@pytest.fixture
def social_app(db):
    """A fixture that creates a Vipps SocialApp instance for tests."""
    app = SocialApp.objects.create(
        provider="vipps",
        name="Vipps Test",
        client_id="test_client_id",
        secret="test_secret",
    )
    app.sites.set([Site.objects.get_current()])
    return app


@pytest.mark.django_db
def test_provider_properties(rf, social_app): # <-- Add social_app fixture
    """Test that the provider has the correct basic properties."""
    request = rf.get('/')
    # Pass the app object during initialization
    provider = VippsProvider(request=request, app=social_app)
    assert provider.id == 'vipps'
    assert provider.name == 'Vipps'

def test_extract_uid(rf, social_app): # <-- Add fixtures
    """Test that the UID is correctly extracted from the user data."""
    request = rf.get('/')
    provider = VippsProvider(request=request, app=social_app)
    data = {'sub': 'user-unique-id-123', 'name': 'Test User'}
    assert provider.extract_uid(data) == 'user-unique-id-123'

def test_extract_common_fields(rf, social_app): # <-- Add fixtures
    """Test that user data is correctly mapped to common Django user fields."""
    request = rf.get('/')
    provider = VippsProvider(request=request, app=social_app)
    data = {
        'sub': 'user-unique-id-123',
        'name': 'Ola Nordmann',
        'given_name': 'Ola',
        'family_name': 'Nordmann',
        'email': 'ola@example.com',
        'email_verified': True,
        'phoneNumber': '4712345678'
    }
    fields = provider.extract_common_fields(data)
    assert fields['email'] == 'ola@example.com'
    assert fields['first_name'] == 'Ola'
    assert fields['last_name'] == 'Nordmann'

def test_extract_extra_data(rf, social_app): # <-- Add fixtures
    """Test that the full data payload is stored in extra_data."""
    request = rf.get('/')
    provider = VippsProvider(request=request, app=social_app)
    data = {'sub': '123', 'phoneNumber': '4712345678', 'name': 'Test'}
    extra_data = provider.extract_extra_data(data)
    assert extra_data['phoneNumber'] == '4712345678'
    assert extra_data['name'] == 'Test'