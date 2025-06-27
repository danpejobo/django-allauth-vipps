# tests/test_provider.py
import pytest
from vipps_auth.provider import VippsProvider

@pytest.mark.django_db
def test_provider_properties():
    """Test that the provider has the correct basic properties."""
    provider = VippsProvider()
    assert provider.id == 'vipps'
    assert provider.name == 'Vipps'

def test_extract_uid():
    """Test that the UID is correctly extracted from the user data."""
    provider = VippsProvider()
    data = {'sub': 'user-unique-id-123', 'name': 'Test User'}
    assert provider.extract_uid(data) == 'user-unique-id-123'

def test_extract_common_fields():
    """Test that user data is correctly mapped to common Django user fields."""
    provider = VippsProvider()
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

def test_extract_extra_data():
    """Test that the full data payload is stored in extra_data."""
    provider = VippsProvider()
    data = {'sub': '123', 'phoneNumber': '4712345678', 'name': 'Test'}
    extra_data = provider.extract_extra_data(data)
    assert extra_data['phoneNumber'] == '4712345678'
    assert extra_data['name'] == 'Test'