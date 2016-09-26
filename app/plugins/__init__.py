from core.services import registry
from django.conf import settings
from core import signals


def register(plugin, *args, **kwargs):
    registry.register(plugin, *args, **kwargs)
    
