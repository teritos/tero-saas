from core.services import registry

def register(plugin, *args, **kwargs):
    registry.register(plugin, *args, **kwargs)
    

ENABLED = [
    'plugins.users'
]


for name in ENABLED:
    __import__(name)
