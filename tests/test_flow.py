# tests/test_flow.py

import pytest
from unittest.mock import patch
from allauth.socialaccount.models import SocialApp
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from vipps_auth.settings import vipps_auth_settings

MOCKED_VIPPS_USER_DATA = {
    'sub': 'vipps-user-12345',
    'name': 'Kari Nordmann',
    'given_name': 'Kari',
    'family_name': 'Nordmann',
    'email': 'kari.nordmann@example.com',
    'email_verified': True,
    'phone_number': '4798765432'
}

@pytest.mark.django_db
class TestVippsLoginFlow:
    """Tests the full social login flow from code to token."""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        """Setup the SocialApp for Vipps in the test database."""
        if not SocialApp.objects.filter(provider='vipps').exists():
            app = SocialApp.objects.create(
                provider='vipps',
                name='Vipps Test App',
                client_id='test-client-id',
                secret='test-client-secret',
            )
            site = Site.objects.get_current()
            app.sites.set([site])
        self.client = client
    
    # THE REAL FIX:
    # We patch the underlying method in allauth's OAuth2 client that
    # actually performs the token exchange. This is much more stable.
    @patch('allauth.socialaccount.providers.oauth2.client.OAuth2Client.get_access_token')
    def test_vipps_login_api_flow(self, mock_get_access_token, requests_mock):
        """
        Simulates a frontend sending an auth code to our API and receiving a JWT.
        """
        # 1. Arrange
        
        # Mock the return value of the token exchange with Vipps
        mock_get_access_token.return_value = {
            'access_token': 'mock_access_token',
            'token_type': 'Bearer',
        }
        
        # Mock the HTTP GET request to the Vipps userinfo endpoint
        profile_url = f'{vipps_auth_settings.BASE_URL}/vipps-userinfo-api/userinfo'
        requests_mock.get(profile_url, json=MOCKED_VIPPS_USER_DATA, status_code=200)

        login_url = reverse('vipps_login_api')

        # 2. Act
        payload = {'code': 'some_vipps_auth_code'}
        response = self.client.post(login_url, payload, format='json')

        # 3. Assert
        assert response.status_code == 200, f"Login failed: {response.data}"
        
        assert 'access' in response.data
        assert 'refresh' in response.data
        
        User = get_user_model()
        assert User.objects.filter(email='kari.nordmann@example.com').exists()
        
        user = User.objects.get(email='kari.nordmann@example.com')
        assert user.first_name == 'Kari'
        assert user.socialaccount_set.filter(provider='vipps', uid='vipps-user-12345').exists()