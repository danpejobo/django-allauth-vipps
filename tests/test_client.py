# tests/test_client.py
import pytest
from django.test import RequestFactory
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from vipps_auth.client import VippsOAuth2Client

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
def test_vipps_oauth2_client_sets_basic_auth(social_app):
    """
    Verify that the custom VippsOAuth2Client correctly sets
    the `basic_auth` flag to True.
    """
    request = RequestFactory().get('/')
    
    # This call must match the new __init__ signature of our client
    client = VippsOAuth2Client(
        request=request,
        consumer_key=social_app.client_id,
        consumer_secret=social_app.secret,
        access_token_method='POST',
        access_token_url='https://example.com/token',
        callback_url='https://example.com/callback',
        scope=['openid', 'name'] # This argument is required by our __init__
    )

    assert client.basic_auth is True