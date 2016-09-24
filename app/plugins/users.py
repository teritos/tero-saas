from plugins import register


class UserService(object):

    name = 'pirulin'

    def __init__(self, frula, foo=None):
        self.frula = frula 
        self.foo = foo

    def ping(self):
        print('ping ping ping!')


register(UserService, 'pirulin', foo='bar')