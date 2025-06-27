# vipps_auth/provider.py

from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.account.adapter import get_adapter

# Import our configurable settings
from .settings import vipps_auth_settings

class VippsAccount(ProviderAccount):
    def to_str(self):
        return self.account.extra_data.get('name', super().to_str())

class VippsProvider(OAuth2Provider):
    id = 'vipps'
    name = 'Vipps'
    account_class = VippsAccount

    def __init__(self, *args, **kwargs):
        """
        Dynamically set the endpoint URLs from our settings object.
        This allows the user to switch between test and production by changing
        the BASE_URL in their settings.py.
        """
        super().__init__(*args, **kwargs)
        base_url = vipps_auth_settings.BASE_URL
        self.access_token_url = f'{base_url}/access-management-1.0/access/oauth2/token'
        self.authorize_url = f'{base_url}/access-management-1.0/access/oauth2/auth'
        self.profile_url = f'{base_url}/vipps-userinfo-api/userinfo'

    def get_default_scope(self):
        """
        Returns the scopes from our configurable settings object.
        """
        return vipps_auth_settings.SCOPES

    def extract_uid(self, data):
        """
        Extracts the unique user ID ('sub' claim). This is a stable identifier from Vipps.
        """
        uid = data.get('sub')
        if not uid:
            get_adapter().error(
                "Vipps user data did not contain a 'sub' identifier, which is required."
            )
        return str(uid)

    def extract_common_fields(self, data):
        """
        Maps standard claims from Vipps to the Django User model.
        """
        return {
            'email': data.get('email'),
            'first_name': data.get('given_name'),
            'last_name': data.get('family_name'),
        }
        
    def extract_extra_data(self, data):
        """
        Saves all other data received from the userinfo endpoint into the
        SocialAccount's `extra_data` JSON field. This is useful for accessing
        non-standard fields like phone_number or nin later.
        """
        return data

    def sociallogin_from_response(self, request, response):
        """
        Performs validation checks on the user data received from Vipps before creating
        the SocialLogin object that represents the session.
        """
        adapter = get_adapter()

        # Check for our EMAIL_VERIFIED_REQUIRED setting.
        if vipps_auth_settings.EMAIL_VERIFIED_REQUIRED:
            email_verified = response.get('email_verified', False)
            if not email_verified:
                adapter.error("Login cancelled: Email from Vipps is not verified.")
                # This will stop the login process and show an error to the user.

        return super().sociallogin_from_response(request, response)