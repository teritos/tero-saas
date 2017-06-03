"""Settings for devel."""

import os

from settings.base_settings import *  # pylint: disable=W0614,W0401

DEBUG = True

ALLOWED_HOSTS = ['*']
FULL_DOMAIN = 'http://127.0.0.1:8000'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tero',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'pgsql',
    }
}

CORS_ORIGIN_ALLOW_ALL = True
ONE_SIGNAL_APP_ID = os.getenv('ONE_SIGNAL_APP_ID')
ONE_SIGNAL_TOKEN  = os.getenv('ONE_SIGNAL_TOKEN')
