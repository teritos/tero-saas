import abc


class ServiceRegistry(object):
 
    def __init__(self):
        self.observers = {} 
        self.hooks = {
            'create_user': [],
        }
 
    def register(self, observer, *args, **kwargs):
        if getattr(observer, 'create_user', None):
            self.hooks['create_user'].append(observer.name)
        self.observers[observer.name] = observer(*args, **kwargs)
 
    def unregister(self, observer):
        del self.observers[observer.name]

    def unregister_all(self):
        self.observers = {}

    def get_service(self, name):
        return self.observers[name]

    def name(self):
        """Service name"""


class Service(object):
    """Service Meta"""


registry = ServiceRegistry()