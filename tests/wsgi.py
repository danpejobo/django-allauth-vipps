# tests/wsgi.py

import os
from django.core.wsgi import get_wsgi_application

# Ensure Django uses the correct settings file for our test app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')

application = get_wsgi_application()