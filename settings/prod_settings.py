"""Production settings."""

import raven
from settings.base_settings import *  # pylint: disable=W0614,W0401

DEBUG = False
TERO_LOG_DIR = '/logs'

ALLOWED_HOSTS = ['tero.ninsei.tk']
FULL_DOMAIN = 'https://tero.ninsei.tk'

STATIC_ROOT = os.getenv('DJANGO_STATIC_ROOT')
MEDIA_ROOT = os.getenv('DJANGO_MEDIA_ROOT')

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PGSQL_NAME'),
        'USER': os.getenv('PGSQL_USER'),
        'PASSWORD': os.getenv('PGSQL_SECRET'),
        'HOST': os.getenv('PGSQL_HOST'),
        'PORT': os.getenv('PGSQL_PORT', '5432'),
    }
}

RAVEN_CONFIG = {
    'dsn': os.getenv('SENTRY_DSN'),
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}

# OneSignal app
ONE_SIGNAL_APP_ID = os.getenv('ONE_SIGNAL_APP_ID')
ONE_SIGNAL_TOKEN  = os.getenv('ONE_SIGNAL_TOKEN')

