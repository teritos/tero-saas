#!/usr/bin/env python
import os
import sys
import django

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
        return self.user_table[username]['home']


def main():
    django.setup()
    authorizer = SoldierAuthorizer()
    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer(('', 2121), handler)
    server.serve_forever()

