#!/usr/bin/env python
import django

from django.conf import settings
from django.contrib.auth import authenticate
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed


class FTPAuthorizer(DummyAuthorizer):

    user_table = {}

    def validate_authentication(self, username, password, handler):
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed
        perm = 'elw'  # CWD, LIST and STOR
        homedir = user.ftpuser.homedir
        msg_login = 'Welcome aboard user!'
        msg_quit = 'See you soon!'
        dic = {'home': homedir,
               'perm': perm,
               'operms': {},
               'msg_login': str(msg_login),
               'msg_quit': str(msg_quit)
               }
        self.user_table[username] = dic


def main():
    django.setup()
    authorizer = FTPAuthorizer()
    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer(('', settings.FTPD_PORT), handler)
    server.serve_forever()
