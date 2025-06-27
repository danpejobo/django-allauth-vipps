# vipps_auth/settings.py
from django.conf import settings

# Define a single dictionary for all our settings for clean namespace in the project's settings.
# For example, in the main project, the user will define:
# VIPPS_AUTH_SETTINGS = { 'BASE_URL': 'https://api.vipps.no' }
USER_SETTINGS = getattr(settings, "VIPPS_AUTH_SETTINGS", {})

# Define the defaults for our package.
DEFAULTS = {
    # The base URL for the Vipps API. Can be overridden for production.
    "BASE_URL": "https://apitest.vipps.no",
    
    # The scopes (permissions) to request from the user.
    "SCOPES": [
        "openid",
        "name",
        "email",
        "phoneNumber",
    ],
    
    # A security flag. If True, the login will fail if Vipps reports the user's email is not verified.
    "EMAIL_VERIFIED_REQUIRED": True,
}

class VippsAuthSettings:
    """
    A settings object that allows our app's settings to be accessed as
    attributes. For example: `vipps_auth_settings.BASE_URL`.
    """
    def __init__(self, user_settings=None, defaults=None):
        if user_settings:
            self._user_settings = user_settings
        self.defaults = defaults or {}

    def __getattr__(self, attr):
        # Check if the user has defined the setting in their project's settings.py
        if attr in self._user_settings:
            return self._user_settings[attr]
        # Otherwise, fall back to our package's default.
        if attr in self.defaults:
            return self.defaults[attr]
        # If the setting doesn't exist at all, raise an error.
        raise AttributeError(f"Invalid Vipps Auth setting: '{attr}'")

# Instantiate the settings object that the rest of our package will use.
vipps_auth_settings = VippsAuthSettings(USER_SETTINGS, DEFAULTS)