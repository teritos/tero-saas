"""FTPD management command."""
from django.conf import settings
from django.core.management.base import BaseCommand
from ftpd.server import TeroFTPServer


class Command(BaseCommand):
    """FTPD command"""
    help = 'Run FTPD server'

    def handle(self, *args, **options):
        host = settings.FTPD_HOST
        port = settings.FTPD_PORT
        rootdir = settings.FTPD_ROOT
        ftp_server = TeroFTPServer(host, port, rootdir)
        ftp_server.run()
