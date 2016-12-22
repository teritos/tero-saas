import os
import logging
import datetime

import requests
from base64 import b64encode

from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer, ThreadedFTPServer, MultiprocessFTPServer
from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed

from django.conf import settings
from django.contrib.auth import authenticate

from settings.asgi import channel_layer
from ftpd.models import FTPAccount
from ftpd.images import ImageHandler

from alarm.models import Alarm
from pathlib import PurePath


logger = logging.getLogger("ftpd")


class FTPDjangoUserAuthorizer(DummyAuthorizer):
    """
    FTPD Authorizer that use DJANGO users decorated with FTPUser model
    """

    def __init__(self, rootdir):
        self.root = rootdir
        super(FTPDjangoUserAuthorizer, self).__init__()

    def validate_authentication(self, username, password, handler):
        """Validate user and password."""
        _ = handler
        logger.info("Authenticating user %s...", username)
        user = authenticate(username=username, password=password)
        if not user:
            logger.info('Authentication failed for user %s with password %s', username, password)
            raise AuthenticationFailed()

        if not Alarm.is_active_for(username):
            logger.info('User %s alarm is deactivated, ignoring session', username)
            raise AuthenticationFailed()

        try:
            ftp_user = FTPAccount.objects.get(alarm__owner=user)
            homedir = ftp_user.homedir
            perm = ftp_user.ftpd_perm
            root_homedir = os.path.join(self.root, homedir)
            os.makedirs(root_homedir, exist_ok=True)
            if not self.has_user(username):
                self.add_user(username, password, root_homedir, perm)
        except FTPAccount.DoesNotExist:
            logger.info(
                "User %s with password %s doesnt have an FTPAccount related object.",
                username,
                password
                )
            raise AuthenticationFailed()


class NotificationFTPHandler(FTPHandler):
    """Tero FTP Handler."""

    passive_ports = list(range(settings.FTPD_PASSIVE_PORTS_MIN, settings.FTPD_PASSIVE_PORTS_MAX))
    masquerade_address = os.getenv('FTPD_MASQUERADE_ADDRESS')

    def __init__(self, conn, server, ioloop=None):
        logger.debug("Initializing FTP Notification handler...")
        super(NotificationFTPHandler, self).__init__(conn, server, ioloop)

    def on_connect(self):
        """User connected."""
        logger.debug("%s:%s connected", self.remote_ip, self.remote_port)

    def on_disconnect(self):
        """User disconnected."""
        logger.debug("%s:%s disconnected", self.remote_ip, self.remote_port)

    def on_login(self, username):
        """User logs in."""
        logger.debug("%s logged in!", username)

    def on_logout(self, username):
        """User logs out."""
        logger.debug("%s logged out!", username)

    def on_file_received(self, filepath):
        """File received."""
        logger.info("File received %s", filepath)
        self._send_notifications(filepath)

    def on_incomplete_file_received(self, filepath):
        """Incomplete File received."""
        logger.info("Incomplete file received %s", filepath)
        self._send_notifications(filepath)

    def _send_notifications(self, filepath):
        """Send a notification."""
        channel_layer.send('mordor.see', {
            'path': filepath,
            'purePath': PurePath(filepath),
            'username': self.username,
            'datetime': datetime.datetime.now().strftime('%d/%m/%Y %h:%m:%s')
        })


class ColoProxyFTPHandler(NotificationFTPHandler):
    """Colo's FTP Handler."""

    def on_file_received(self, filepath):
        """File received."""
        ftp_account = FTPAccount.objects.get(alarm__owner__username=self.username)
        logger.info('Proxy image [%s] for user {%s}', filepath, ftp_account)

        with open(filepath, 'rb') as f:
            filename = f.name.split('/')[-1]
            b64image = b64encode(f.read())

            response = requests.post(settings.IMAGES_PROXY_URL, data={
                'filename': filename,
                'b64image': b64image,
                'alarm_id': ftp_account.alarm.id
            })

            if not response.ok:
                errors = response.json().get('errors')
                logger.error(errors)


class AlarmFTPServer():
    """Tero FTP Server."""

    SERVER_TYPE = ('async', 'threaded', 'multiprocess')

    SERVER_TYPE_CLASS = {'async': FTPServer,
                         'threaded': ThreadedFTPServer,
                         'multiprocess': MultiprocessFTPServer}

    def __init__(self, host, port, rootdir, stype='threaded', handler=NotificationFTPHandler):
        logger.info("Initializing FTP server...")
        self.create_root_dir(rootdir)
        address = (host, port)
        handler = handler
        handler.authorizer = FTPDjangoUserAuthorizer(rootdir)
        server_impl = self.get_server_impl(stype)
        self.ftp_server = server_impl(address, handler)
        self.set_server_settings()

    def get_server_impl(self, stype='threaded'):
        return self.SERVER_TYPE_CLASS.get(stype, ThreadedFTPServer)

    def set_server_settings(self):
        logger.debug("Setting FTPD parameters...")
        self.ftp_server.max_cons = 10000
        self.ftp_server.max_cons_per_ip = 5

    def create_root_dir(self, rootdir):
        logger.info("Creating FTP root dir %s...", rootdir)
        os.makedirs(rootdir, exist_ok=True)

    def run(self):
        """Start FTP server"""
        address, port = self.ftp_server.address
        logger.info("Starting FTP server on: %s:%s", address, port)
        try:
            self.ftp_server.serve_forever()
        finally:
            logger.debug("Server stopped, closing all connections!")
            self.ftp_server.close_all()
