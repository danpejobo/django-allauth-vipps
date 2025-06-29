# tests/settings.py
import os

# Read the public domain from the .env file
TEST_APP_DOMAIN = os.getenv("TEST_APP_DOMAIN", "http://127.0.0.1:8000")

# We point it to the same callback URL that the standard web flow uses.
VIPPS_API_CALLBACK_URL = f"{TEST_APP_DOMAIN}/accounts/vipps/login/callback/"

SECRET_KEY = "dummy-key-for-testing-2fA9dAtV7v2uwPC$SV&%ZQdss^ia@4^&"

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # Third-party apps required for tests
    "rest_framework",
    "rest_framework.authtoken",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth",

    # The app we are testing
    "vipps_auth",
]

# Middelware for testing
MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

# The admin requires a template engine to render its HTML pages.
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

# A dummy database for testing
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/app/db.sqlite3",
    }
}

# Required by django-allauth
SITE_ID = 1

# Point to the test-specific URL configuration
ROOT_URLCONF = "tests.urls"

# Tell Django to use allauth's backend for authentication
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Configure dj-rest-auth to use JWT authentication, which your test expects
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

REST_AUTH = {
    "USE_JWT": True,
}

# Disable email verification to avoid unnecessary confirmation flow in tests
ACCOUNT_EMAIL_VERIFICATION = "none"

# This tells the package to use the Vipps test environment
VIPPS_AUTH_SETTINGS = {
    "BASE_URL": "https://apitest.vipps.no",
}