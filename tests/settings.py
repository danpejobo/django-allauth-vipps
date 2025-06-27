# tests/settings.py
SECRET_KEY = "dummy-key-for-testing"
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    
    # The app we are testing
    "vipps_auth",
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
SITE_ID = 1
ROOT_URLCONF = "tests.urls"