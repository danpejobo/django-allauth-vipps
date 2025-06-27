# tests/urls.py

from django.urls import path, include
from dj_rest_auth.registration.views import SocialLoginView
from vipps_auth.views import VippsOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

class VippsLogin(SocialLoginView):
    adapter_class = VippsOAuth2Adapter
    client_class = OAuth2Client
    # Define the callback_url used during the test flow.
    callback_url = "http://localhost/callback"


urlpatterns = [
    # The API endpoint our test will hit
    path(
        "api/v1/auth/social/vipps/",
        VippsLogin.as_view(),
        name="vipps_login_api"
    ),
    
    # The browser-flow URLs from our package
    path("accounts/", include("vipps_auth.urls")),
]