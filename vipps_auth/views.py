# vipps_auth/views.py

from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

# Import the provider you created
from .provider import VippsProvider

class VippsOAuth2Adapter(OAuth2Adapter):
    """
    This adapter connects the Vipps API flow to the allauth framework.
    It specifies which provider it's for and where to find the API endpoints.
    """
    provider_id = VippsProvider.id

    # The actual URLs are dynamically constructed in your provider,
    # but we can reference them here for clarity. allauth will call
    # your provider instance to get these URLs.
    @property
    def access_token_url(self):
        return self.provider.access_token_url

    @property
    def authorize_url(self):
        return self.provider.authorize_url

    @property
    def profile_url(self):
        return self.provider.profile_url

# These are the actual view functions that will be connected to your URLs.
# We are using the standard, pre-built views from django-allauth and just
# telling them to use our custom Vipps adapter.

# This view initiates the login process by redirecting the user to Vipps.
vipps_login = OAuth2LoginView.adapter_view(VippsOAuth2Adapter)

# This view handles the callback from Vipps after the user has authenticated.
vipps_callback = OAuth2CallbackView.adapter_view(VippsOAuth2Adapter)