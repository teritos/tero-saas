import os
import logging

import requests
from base64 import b64encode

from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer, ThreadedFTPServer, MultiprocessFTPServer
from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed

from django.conf import settings
from django.contrib.auth import authenticate

from apps.ftpd.models import FTPAccount


logger = logging.getLogger("ftpd")


class FTPDjangoUserAuthorizer(DummyAuthorizer):
    """
    FTPD Authorizer that use DJANGO users decorated with FTPUser model
    """

    def __init__(self, rootdir):
        self.root = rootdir
        super(FTPDjangoUserAuthorizer, self).__init__()

    def validate_authentication(self, username, password, handler):
        logger.info("Authenticating user %s...", username)
        user = authenticate(username=username, password=password)
        msg = "Authentication failed."
        if not user:
            logger.error(msg)
            logger.debug("Django user does not exist!")
            raise AuthenticationFailed(msg)
        try:
            ftp_user = FTPAccount.objects.get(alarm__owner=user)
            homedir = ftp_user.homedir
            perm = ftp_user.ftpd_perm
            root_homedir = os.path.join(self.root, homedir)
            os.makedirs(root_homedir, exist_ok=True)
            if not self.has_user(username):
                self.add_user(username, password, root_homedir, perm)
        except FTPAccount.DoesNotExist:
            logger.error(msg)
            logger.debug("FTP user does not exist!")
            raise AuthenticationFailed(msg)


class NotificationFTPHandler(FTPHandler):

    def __init__(self, conn, server, ioloop=None):
        logger.debug("Initializing FTP Notification handler...")
        super(NotificationFTPHandler, self).__init__(conn, server, ioloop)

    def on_connect(self):
        logger.debug("%s:%s connected", self.remote_ip, self.remote_port)

    def on_disconnect(self):
        logger.debug("%s:%s disconnected", self.remote_ip, self.remote_port)

    def on_login(self, username):
        logger.debug("%s logged in!", username)

    def on_logout(self, username):
        logger.debug("%s logged out!", username)

    def on_file_received(self, filepath):
        logger.info("File received %s", filepath)
        self._send_notifications(filepath)

    def on_incomplete_file_received(self, filepath):
        logger.info("Incomplete file received %s", filepath)
        self._send_notifications(filepath)

    def _send_notifications(self, filepath):
        logger.info("Firing notification...")
        ftp_user = FTPAccount.objects.get(alarm__owner__username=self.username)
        logger.info('trigger {}'.format(ftp_user.alarm))


class ProxyFTPHandler(FTPHandler):

    def __init__(self, conn, server, ioloop=None):
        logger.debug("Initializing Proxy FTP handler...")
        super(ProxyFTPHandler, self).__init__(conn, server, ioloop)

    def on_connect(self):
        logger.debug("%s:%s connected", self.remote_ip, self.remote_port)

    def on_disconnect(self):
        logger.debug("%s:%s disconnected", self.remote_ip, self.remote_port)

    def on_login(self, username):
        logger.debug("%s logged in!", username)

    def on_logout(self, username):
        logger.debug("%s logged out!", username)

    def on_incomplete_file_received(self, filepath):
        logger.info("Incomplete file received %s", filepath)

    def on_file_received(self, filepath):
        ftp_account = FTPAccount.objects.get(alarm__owner__username=self.username)
        logger.info('Proxy image [{}] for user {}'.format(filepath, ftp_account))
        
        with open(filepath, 'rb') as f:
            filename = f.name.split('/')[-1]
            b64image = b64encode(f.read())

            r = requests.post(settings.IMAGES_PROXY_URL, data={
                'filename': filename,
                'b64image': b64image,
                'alarm_id': ftp_account.alarm.id
            })

            if not r.ok:
                errors = r.json().get('errors')
                logger.error(errors)

        #os.remove(filepath)


class AlarmFTPServer():

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
        logger.info("Starting FTP server on: %s:%s" % self.ftp_server.address)
        try:
            self.ftp_server.serve_forever()
        finally:
            logger.debug("Server stopped, closing all connections!")
            self.ftp_server.close_all()
