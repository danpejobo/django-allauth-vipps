# tests/urls.py

from django.urls import path, include
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

# Import the adapters we need
from vipps_auth.views import VippsOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter


# --- The Vipps View (Subclassing is Required) ---
class VippsLogin(SocialLoginView):
    adapter_class = VippsOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://localhost/callback/vipps"

# --- The Google View (Subclassing is Required) ---
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://localhost/callback/google"


urlpatterns = [
    # Vipps API endpoint using the required subclass
    path(
        "api/v1/auth/social/vipps/",
        VippsLogin.as_view(),
        name="vipps_login_api"
    ),

    # Google API endpoint using the required subclass
    path(
        "api/v1/auth/social/google/",
        GoogleLogin.as_view(),
        name="google_login_api"
    ),
    
    # Browser-flow URLs from our package
    path("accounts/", include("vipps_auth.urls")),
]