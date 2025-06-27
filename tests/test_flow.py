# tests/test_flow.py
import pytest
from unittest.mock import patch
from allauth.socialaccount.models import SocialApp
from django.urls import reverse # Import reverse
from django.contrib.auth import get_user_model # Import get_user_model

# We will use this to simulate API responses from Vipps
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
    def setup(self, client): # No need for 'db' fixture, pytest-django handles it
        """Setup the SocialApp for Vipps in the test database."""
        if not SocialApp.objects.filter(provider='vipps').exists():
            SocialApp.objects.create(
                provider='vipps',
                name='Vipps Test App',
                client_id='test-client-id',
                secret='test-client-secret',
                sites_string='1' # Use sites_string for newer versions if needed
            )
        self.client = client
    
    @patch('allauth.socialaccount.providers.oauth2.views.OAuth2Adapter.get_access_token_data')
    @patch('allauth.socialaccount.providers.oauth2.views.OAuth2Adapter.get_profile_info')
    def test_vipps_login_api_flow(self, mock_get_profile_info, mock_get_access_token):
        """
        Simulates a frontend sending an auth code to our API and receiving a JWT.
        """
        # 1. Arrange
        mock_get_access_token.return_value = {
            'access_token': 'mock_access_token',
            'token_type': 'Bearer',
        }
        mock_get_profile_info.return_value = MOCKED_VIPPS_USER_DATA

        # Use reverse() to get the URL dynamically
        login_url = reverse('vipps_login_api')

        # 2. Act
        payload = {'code': 'some_vipps_auth_code'}
        response = self.client.post(login_url, payload, format='json')

        # 3. Assert
        assert response.status_code == 200, f"Login failed: {response.data}"
        
        # dj-rest-auth with SimpleJWT returns 'access' and 'refresh' by default
        assert 'access' in response.data
        assert 'refresh' in response.data
        
        User = get_user_model()
        assert User.objects.filter(email='kari.nordmann@example.com').exists()
        
        user = User.objects.get(email='kari.nordmann@example.com')
        assert user.first_name == 'Kari'
        assert user.socialaccount_set.filter(provider='vipps', uid='vipps-user-12345').exists()