# tests/test_flow.py

import pytest
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth import get_user_model

# The import of vipps_auth_settings is no longer needed

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

    # The setup fixture that created a SocialApp in the DB is no longer needed.
    # allauth will automatically use the app configured in tests/settings.py.

    @patch('allauth.socialaccount.providers.oauth2.client.OAuth2Client.get_access_token')
    def test_vipps_login_api_flow(self, mock_get_access_token, requests_mock, client):
        """
        Simulates a frontend sending an auth code to our API and receiving a JWT.
        """
        # 1. Arrange
        mock_get_access_token.return_value = {
            'access_token': 'mock_access_token',
            'token_type': 'Bearer',
        }

        # Since tests run with TEST_MODE=True, we know the expected base URL
        base_url = "https://apitest.vipps.no"
        profile_url = f'{base_url}/vipps-userinfo-api/userinfo'
        requests_mock.get(profile_url, json=MOCKED_VIPPS_USER_DATA, status_code=200)

        login_url = reverse('vipps_login_api')

        # 2. Act
        payload = {'code': 'some_vipps_auth_code'}
        response = client.post(login_url, payload, format='json')

        # 3. Assert
        assert response.status_code == 200, f"Login failed: {response.data}"

        assert 'access' in response.data
        assert 'refresh' in response.data

        User = get_user_model()
        user = User.objects.get(email='kari.nordmann@example.com')
        assert user.first_name == 'Kari'
        assert user.socialaccount_set.filter(provider='vipps', uid='vipps-user-12345').exists()