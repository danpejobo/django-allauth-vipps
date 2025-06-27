from dj_rest_auth.registration.views import SocialLoginView
from vipps_auth.views import VippsOAuth2Adapter

class VippsLogin(SocialLoginView):
    adapter_class = VippsOAuth2Adapter

urlpatterns = [
    path('api/v1/auth/social/vipps/', VippsLogin.as_view(), name='vipps_login_api'),
    path('accounts/', include('vipps_auth.urls')), # For browser-based flow

]