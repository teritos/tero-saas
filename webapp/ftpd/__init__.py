#!/usr/bin/env python
import os
import django

from django.conf import settings
from django.contrib.auth import authenticate
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed


class SoldierAuthorizer(DummyAuthorizer):

    def validate_authentication(self, username, password, handler):
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed

    def get_home_dir(self, username):
        """Return the user's home directory.
        """
        homedir = os.path.join(settings.FTPD_ROOT_DIR, username)
        if not os.path.isdir(homedir):
            os.makedirs(homedir)
        return homedir

    def get_msg_login(self, username):
        return "Welcome back {}".format(username)


def main():
    django.setup()
    authorizer = SoldierAuthorizer()
    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer(('', settings.FTPD_PORT), handler)
    server.serve_forever()
