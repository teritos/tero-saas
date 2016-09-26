from core.services import registry
from core.models import Alarm
from django.conf import settings
from core import signals


def register(plugin, *args, **kwargs):
    registry.register(plugin, *args, **kwargs)
    

PLUGINS_ENABLED = []

for name in settings.SETTINGS_YAML['PLUGINS']:
    plugin_name = 'plugin.' + name 
    PLUGINS_ENABLED.append(plugin_name)

settings.INSTALLED_APPS += PLUGINS_ENABLED


for plugin in PLUGINS_ENABLED:
    print('Loading plugin {}...'.format(plugin))
    __import__(name)
