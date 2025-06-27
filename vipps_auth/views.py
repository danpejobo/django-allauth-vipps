# vipps_auth/views.py

from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)
from .provider import VippsProvider

class VippsOAuth2Adapter(OAuth2Adapter):
    provider_id = VippsProvider.id

    # THE FIX, PART 2:
    # The adapter must also have these attributes for dj-rest-auth to find.
    # We simply point them to the definitive URLs on our provider class.
    access_token_url = VippsProvider.access_token_url
    authorize_url = VippsProvider.authorize_url
    profile_url = VippsProvider.profile_url


# These standard views use our adapter and provider correctly.
vipps_login = OAuth2LoginView.adapter_view(VippsOAuth2Adapter)
vipps_callback = OAuth2CallbackView.adapter_view(VippsOAuth2Adapter)