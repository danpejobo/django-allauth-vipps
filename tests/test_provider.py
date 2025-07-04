# tests/test_provider.py
import pytest
from django.test import override_settings
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from vipps_auth.provider import VippsProvider


@pytest.fixture
def social_app(db):
    """A fixture that creates a Vipps SocialApp instance for tests."""
    app = SocialApp.objects.create(
        provider="vipps",
        name="Vipps Test",
        client_id="test_client_id",
        secret="test_secret",
    )
    app.sites.add(Site.objects.get_current())
    return app


@pytest.mark.django_db
def test_provider_properties(rf, social_app):
    provider = VippsProvider(request=rf.get('/'), app=social_app)
    assert provider.id == 'vipps'
    assert provider.name == 'Vipps'


@pytest.mark.django_db
def test_get_base_url(rf, social_app):
    """Test that the base URL changes based on the TEST_MODE setting."""
    # The test suite is configured with TEST_MODE=True by default in tests/settings.py
    provider = VippsProvider(request=rf.get('/'), app=social_app)
    assert provider.get_base_url() == "https://apitest.vipps.no"

    # Override settings to specifically disable test mode and check for production URL
    with override_settings(SOCIALACCOUNT_PROVIDERS={'vipps': {'TEST_MODE': False}}):
        provider = VippsProvider(request=rf.get('/'), app=social_app)
        assert provider.get_base_url() == "https://api.vipps.no"


@pytest.mark.django_db
def test_extract_uid(rf, social_app):
    provider = VippsProvider(request=rf.get('/'), app=social_app)
    data = {'sub': 'user-unique-id-123', 'name': 'Test User'}
    assert provider.extract_uid(data) == 'user-unique-id-123'


@pytest.mark.django_db
def test_extract_common_fields(rf, social_app):
    provider = VippsProvider(request=rf.get('/'), app=social_app)
    data = {
        'sub': 'user-unique-id-123',
        'name': 'Ola Nordmann',
        'given_name': 'Ola',
        'family_name': 'Nordmann',
        'email': 'ola@example.com',
    }
    fields = provider.extract_common_fields(data)
    assert fields['email'] == 'ola@example.com'
    assert fields['first_name'] == 'Ola'
    assert fields['last_name'] == 'Nordmann'