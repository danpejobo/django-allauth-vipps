# tests/settings.py
import os

# Read the public domain from the .env file
TEST_APP_DOMAIN = os.getenv("TEST_APP_DOMAIN", "http://127.0.0.1:8000")

# We point it to the same callback URL that the standard web flow uses.
VIPPS_API_CALLBACK_URL = f"{TEST_APP_DOMAIN}/accounts/vipps/login/callback/"

SECRET_KEY = "dummy-key-for-testing-2fA9dAtV7v2uwPC$SV&%ZQdss^ia@4^&"

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "rest_framework",
    "rest_framework.authtoken",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth",
    "vipps_auth", # The app we are testing
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/app/db.sqlite3",
    }
}

SITE_ID = 1
ROOT_URLCONF = "tests.urls"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

REST_AUTH = {"USE_JWT": True}
ACCOUNT_EMAIL_VERIFICATION = "none"

# Replace VIPPS_AUTH_SETTINGS with the standard allauth configuration
SOCIALACCOUNT_PROVIDERS = {
    'vipps': {
        # Configure credentials directly for self-contained tests
        'APPS': [
            {
                'client_id': 'test-client-id',
                'secret': 'test-client-secret',
                'key': ''
            }
        ],
        # Ensure the tests use the Vipps test environment
        'TEST_MODE': True,
    }
}