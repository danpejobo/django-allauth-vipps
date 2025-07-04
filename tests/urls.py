# tests/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from dj_rest_auth.registration.views import SocialLoginView
# Import the actual client from the package
from vipps_auth.client import VippsOAuth2Client
from vipps_auth.views import VippsOAuth2Adapter

# The VippsTestClient class is no longer needed and can be deleted.

class VippsLogin(SocialLoginView):
    adapter_class = VippsOAuth2Adapter
    # Use the real client from the package now.
    client_class = VippsOAuth2Client
    callback_url = settings.VIPPS_API_CALLBACK_URL


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/auth/social/vipps/",
        VippsLogin.as_view(),
        name="vipps_login_api"
    ),
    path("accounts/", include("vipps_auth.urls")),
    path('accounts/', include('allauth.urls')),
]