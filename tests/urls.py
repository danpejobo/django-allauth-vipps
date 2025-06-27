# Create this new file: tests/urls.py

from django.urls import path, include
from dj_rest_auth.registration.views import SocialLoginView
from vipps_auth.views import VippsOAuth2Adapter

# This view is for the dj-rest-auth social login flow.
class VippsLogin(SocialLoginView):
    adapter_class = VippsOAuth2Adapter

urlpatterns = [
    # The API endpoint our test will hit
    path(
        "api/v1/auth/social/vipps/",
        VippsLogin.as_view(),
        name="vipps_login_api" # Give it a name to use with reverse()
    ),
    
    # The browser-flow URLs from our package
    path("accounts/", include("vipps_auth.urls")),
]