#!/usr/bin/env python
import django
import threading
import plugins.ftpd.signals

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
        perm = 'elradfmwM'  # CWD, LIST and STOR
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


class MyFTPHandler(FTPHandler):

    def get_user_alarm(self):
        from core.models import UserProfile
        user_profile = UserProfile.objects.get(user__username=self.username)
        return user_profile.alarm

    def on_file_received(self, filepath):
        alarm = self.get_user_alarm()
        t = threading.Thread(target=alarm.trigger_motion_detected, args=(filepath,))
        t.start()
        # alarm.notify_motion_detected(file)

    def on_incomplete_file_received(self, file):
        alarm = self.get_user_alarm()
        # alarm.notify_motion_detected(file)
        t = threading.Thread(target=alarm.trigger_motion_detected, args=(filepath,))
        t.start()


def main():
    django.setup()
    authorizer = FTPAuthorizer()
    handler = MyFTPHandler
    handler.authorizer = authorizer
    server = FTPServer(('', settings.FTPD_PORT), handler)
    server.serve_forever()
