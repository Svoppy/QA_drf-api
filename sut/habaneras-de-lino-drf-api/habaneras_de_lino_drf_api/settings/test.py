"""
Test settings — uses SQLite in-memory DB, no external services required.
Used by: pytest (unit tests only)
"""
from .base import *

SECRET_KEY = 'test-secret-key-for-qa-unit-tests'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Only keep apps needed for unit tests — removes UI/cloud dependencies
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'django_filters',
    'rest_framework',
    'store_app',
    'admin_app',
]

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/tmp/test_media/'

STRIPE_PUBLISHABLE_KEY = 'pk_test_placeholder'
STRIPE_SECRET_KEY = 'sk_test_placeholder'

CORS_ALLOWED_ORIGINS = ['http://localhost:3000']
