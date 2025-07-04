# tests/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from vipps_auth.views import VippsOAuth2Adapter


# WORKAROUND for dj-rest-auth and newer django-allauth versions.
# dj-rest-auth passes `scope` as a positional argument, but the new
# OAuth2Client.__init__ does not accept it. We create a shim class
# that accepts the argument but ignores it.
class VippsTestClient(OAuth2Client):
    def __init__(self, request, consumer_key, consumer_secret,
                 access_token_method, access_token_url, callback_url,
                 scope, **kwargs):
        super().__init__(request, consumer_key, consumer_secret,
                         access_token_method, access_token_url, callback_url,
                         **kwargs)


class VippsLogin(SocialLoginView):
    adapter_class = VippsOAuth2Adapter
    # Use our workaround client class for the test API view
    client_class = VippsTestClient
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