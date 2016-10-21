import os
import logging

from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer, ThreadedFTPServer, MultiprocessFTPServer
from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed

from django.contrib.auth import authenticate

from ftpd.models import FTPUser


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
            ftp_user = FTPUser.objects.get(user=user)
            homedir = ftp_user.homedir
            perm = ftp_user.ftpd_perm
            root_homedir = os.path.join(self.root, homedir)
            os.makedirs(root_homedir, exist_ok=True)
            if not self.has_user(username):
                self.add_user(username, password, root_homedir, perm)
        except FTPUser.DoesNotExist:
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

    def on_file_received(self, file):
        logger.info("File received %s", file)
        self._send_notifications(file)

    def on_incomplete_file_received(self, file):
        logger.info("Incomplete file received %s", file)
        self._send_notifications(file)

    def _send_notifications(self, file):
        logger.info("Firing notification...")
        ftp_user = FTPUser.objects.get(user__username=self.username)
        handlers = ftp_user.get_active_notification_handlers()
        data = open(file, 'rb')
        kwarg = {'file': data}
        # TODO: send in a thread or task
        for hdl in handlers:
            hdl.new_notification(kwarg)


class NotificationFTPServer():

    SERVER_TYPE = ('async', 'threaded', 'multiprocess')

    SERVER_TYPE_CLASS = {'async': FTPServer,
                         'threaded': ThreadedFTPServer,
                         'multiprocess': MultiprocessFTPServer}

    def __init__(self, host, port, rootdir, stype='async'):
        logger.info("Initializing FTP server...")
        self.create_root_dir(rootdir)
        address = (host, port)
        handler = NotificationFTPHandler
        handler.authorizer = FTPDjangoUserAuthorizer(rootdir)
        server_impl = self.get_server_impl(stype)
        self.ftp_server = server_impl(address, handler)
        self.set_server_settings()

    def get_server_impl(self, stype='async'):
        return self.SERVER_TYPE_CLASS.get(stype, FTPServer)

    def set_server_settings(self):
        logger.debug("Setting FTPD parameters...")
        self.ftp_server.max_cons = 10
        self.ftp_server.max_cons_per_ip = 2

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
