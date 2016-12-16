import os
import dj_database_url

from settings.base_settings import *

DEBUG = True

ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')

TERO_CONFIG_DIR = os.path.expanduser('~/.config/tero')

STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

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
        'PORT': os.getenv('PGSQL_PORT', '5432',
    }
}

# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

FTPD_HOST = '0.0.0.0'
FTPD_PORT = 2121
FTPD_ROOT = os.path.join(TERO_CONFIG_DIR, 'ftp')
if not os.path.exists(FTPD_ROOT):
    os.makedirs(FTPD_ROOT)


LOGGING_DEFAULT_LEVEL = 'DEBUG'
LOGGING_CONSOLE_HANDLER = 'console'
LOGGING_FILE_HANDLER = 'file_default'
LOGGING_DEFAULT_HANDLERS = [LOGGING_CONSOLE_HANDLER]

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
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'filters': ['require_debug_true'],
        },
    },
    'loggers': {
        'django': {
            'handlers': LOGGING_DEFAULT_HANDLERS,
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': LOGGING_DEFAULT_HANDLERS,
            'level': LOGGING_DEFAULT_LEVEL,
            'propagate': False,
        },
        'ftpd': {
            'handlers': LOGGING_DEFAULT_HANDLERS,
            'level': LOGGING_DEFAULT_LEVEL,
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
