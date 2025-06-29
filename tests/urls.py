# tests/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

# Import the adapters we need
from vipps_auth.views import VippsOAuth2Adapter

# --- The Vipps View (Subclassing is Required) ---
class VippsLogin(SocialLoginView):
    adapter_class = VippsOAuth2Adapter
    client_class = OAuth2Client
    callback_url = settings.VIPPS_API_CALLBACK_URL


urlpatterns = [
    # This makes the admin panel available at /admin/
    path("admin/", admin.site.urls),
    
    # Vipps API endpoint using the required subclass
    path(
        "api/v1/auth/social/vipps/",
        VippsLogin.as_view(),
        name="vipps_login_api"
    ),
    
    # Browser-flow URLs from our package
    path("accounts/", include("vipps_auth.urls")),
    
    # Also include allauth's standard URLs for completeness
    path('accounts/', include('allauth.urls')),
]