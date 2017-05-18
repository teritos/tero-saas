"""Production settings."""

import os
from settings.base_settings import *  # pylint: disable=W0614,W0401

DEBUG = False

ALLOWED_HOSTS = ['tero.ninsei.tk']
FULL_DOMAIN = 'https://tero.ninsei.tk'

STATIC_ROOT = os.getenv('DJANGO_STATIC_ROOT')
MEDIA_ROOT = os.getenv('DJANGO_MEDIA_ROOT')

TERO_ROOT_DIR = os.path.expanduser('~/.tero')
if not os.path.isdir(TERO_ROOT_DIR):
    os.makedirs(TERO_ROOT_DIR)

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Extra places for collectstatic to find static files.
# STATICFILES_DIRS = (
#     os.path.join(PROJECT_ROOT, 'static'),
# )

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

IMAGES_PROXY_URL = 'http://localhost:8000/images/upload'

TERO_LOG_DIR = os.path.join(TERO_ROOT_DIR, 'logs')
if not os.path.exists(TERO_LOG_DIR):
    os.makedirs(TERO_LOG_DIR)
LOGGING_DEFAULT_LEVEL = 'DEBUG'
LOGGING_CONSOLE_HANDLER = 'console'
LOGGING_FILE_HANDLER = 'file_default'
LOGGING_DEFAULT_HANDLERS = [LOGGING_CONSOLE_HANDLER, LOGGING_FILE_HANDLER]

# Logging config
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s %(levelname)s] (%(module)s): %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        LOGGING_CONSOLE_HANDLER: {
            'level': LOGGING_DEFAULT_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'filters': ['require_debug_true'],
        },
        LOGGING_FILE_HANDLER: {
            'level': LOGGING_DEFAULT_LEVEL,
            'class': 'logging.FileHandler',
            'filename': os.path.join(TERO_LOG_DIR, 'dj-tero.log'),
            'formatter': 'verbose',
            'filters': [],
        },
    },
    'loggers': {
        'django': {
            'handlers': [LOGGING_CONSOLE_HANDLER],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': [LOGGING_CONSOLE_HANDLER],
            'level': 'INFO',
            'propagate': False,
        },
        'notifications': {
            'handlers': LOGGING_DEFAULT_HANDLERS,
            'level': LOGGING_DEFAULT_LEVEL,
            'propagate': False,
        },
    }
}

# Django channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.getenv('REDIS_HOST'), 6379)],
        },
        "ROUTING": "settings.routing.channel_routing",
    },
}

# Telegram app
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_API_URL = 'https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/'


# OneSignal app
ONE_SIGNAL_APP_ID = os.getenv('ONE_SIGNAL_APP_ID')
ONE_SIGNAL_TOKEN  = os.getenv('ONE_SIGNAL_TOKEN')

