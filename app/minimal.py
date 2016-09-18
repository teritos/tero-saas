import os
import sys
import yaml

from django.conf import settings
from django.conf.urls import url
from django.core.management import execute_from_command_line
from django.http import HttpResponse


# Load API keys, secrets, etc from yaml file
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
    )
conf = yaml.load(open(os.path.join(BASE_DIR, 'settings.yaml'), 'r'))

settings.configure(
    DEBUG=True,
    SECRET_KEY='A-random-secret-key!',
    ROOT_URLCONF=sys.modules[__name__],
    FTPD_HOST=conf['FTPD']['HOST'],
    FTPD_PORT=conf['FTPD']['PORT'],
    TELEGRAM_BOT_TOKEN=conf['TELEGRAM_BOT']['TOKEN'],
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'ftpd',
    ]
)

def index(request):
    return HttpResponse('<h1>A minimal Django response!</h1>')

urlpatterns = [
    url(r'^$', index),
]

if __name__ == '__main__':
    execute_from_command_line(sys.argv)
