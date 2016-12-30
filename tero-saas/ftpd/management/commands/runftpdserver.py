import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from ftpd.server import AlarmFTPServer, NotificationFTPHandler, ColoProxyFTPHandler


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run FTPD server'

    def add_arguments(self, parser):
        parser.add_argument(
            '-t', '--type',
            default=['threaded'],
            dest='stype',
            choices=AlarmFTPServer.SERVER_TYPE,
            type=str,
            help="Concurrency model used by the FTP server",
            nargs=1,
        )

        parser.add_argument(
            '-p', '--proxy',
            action='store_true'
        )

    def handle(self, *args, **options):

        stype = options['stype'].pop()
        logger.debug("stype: %s", stype)

        host = settings.FTPD_HOST
        port = settings.FTPD_PORT
        rootdir = settings.FTPD_ROOT
        handler = NotificationFTPHandler
        
        if options['proxy']:
            handler = ProxyFTPHandler

        ftp_server = AlarmFTPServer(host, port, rootdir, stype=stype, handler=handler)
        ftp_server.run()
