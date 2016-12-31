"""FTPD Server."""
import os
import logging


from pyftpdlib.servers import ThreadedFTPServer
from ftpd.handlers import DjangoChannelsFTPHandler
from ftpd.authorizer import FTPDjangoUserAuthorizer


logger = logging.getLogger("ftpd")  # pylint: disable=C0103


class TeroFTPServer(object):
    """Tero FTP Server."""

    def __init__(self, host, port, rootdir,
                 server_type=ThreadedFTPServer,
                 handler=DjangoChannelsFTPHandler):
        self.create_root_dir(rootdir)
        address = (host, port)
        handler = handler
        handler.authorizer = FTPDjangoUserAuthorizer(rootdir)
        self.ftp_server = server_type(address, handler)
        self.set_server_settings()

    def set_server_settings(self):
        """Set max_cons, max_cons_per_ip and other settings..."""
        logger.debug("Setting FTPD parameters...")
        self.ftp_server.max_cons = 10000
        self.ftp_server.max_cons_per_ip = 5

    def create_root_dir(self, rootdir):
        """Create directory to place FTPD files."""
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
