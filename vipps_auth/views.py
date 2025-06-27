# vipps_auth/views.py

from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)
from .provider import VippsProvider

class VippsOAuth2Adapter(OAuth2Adapter):
    """
    This adapter connects the Vipps API flow to the allauth framework.
    It simply points to our provider. The allauth views will correctly
    get the endpoint URLs from the provider instance during the request.
    """
    provider_id = VippsProvider.id


# These are the standard, pre-built allauth views. We are just telling
# them to use our custom Vipps adapter.
vipps_login = OAuth2LoginView.adapter_view(VippsOAuth2Adapter)
vipps_callback = OAuth2CallbackView.adapter_view(VippsOAuth2Adapter)