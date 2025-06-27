# tests/settings.py

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
    "allauth.account.middleware.AccountMiddleware", # The middleware the error asked for
]

# A dummy database for testing
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
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