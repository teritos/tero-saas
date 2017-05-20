"""Production settings."""

from settings.base_settings import *  # pylint: disable=W0614,W0401

DEBUG = False

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

# OneSignal app
ONE_SIGNAL_APP_ID = os.getenv('ONE_SIGNAL_APP_ID')
ONE_SIGNAL_TOKEN  = os.getenv('ONE_SIGNAL_TOKEN')

