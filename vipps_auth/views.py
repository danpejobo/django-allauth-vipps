# vipps_auth/views.py

from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)
from .provider import VippsProvider
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
import requests

class VippsOAuth2Adapter(OAuth2Adapter):
    provider_id = VippsProvider.id
    client_class = OAuth2Client

    def complete_login(self, request, app, token, **kwargs):
        """Fetch user info from Vipps and return a populated SocialLogin."""
        provider = self.get_provider()
        profile_url = provider.get_profile_url(request)
        headers = {"Authorization": f"Bearer {token.token}"}

        resp = requests.get(profile_url, headers=headers)
        resp.raise_for_status()
        extra_data = resp.json()

        return provider.sociallogin_from_response(request, extra_data)


vipps_login = OAuth2LoginView.adapter_view(VippsOAuth2Adapter)
vipps_callback = OAuth2CallbackView.adapter_view(VippsOAuth2Adapter)