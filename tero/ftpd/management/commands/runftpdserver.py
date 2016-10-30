import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from ftpd.server import NotificationFTPServer


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run FTPD server'

    def add_arguments(self, parser):
        parser.add_argument('-t', '--type',
                            default=['threaded'],
                            dest='stype',
                            choices=NotificationFTPServer.SERVER_TYPE,
                            type=str,
                            help="Concurrency model used by the FTP server",
                            nargs=1,
                            )

    def handle(self, *args, **options):

        stype = options['stype'].pop()
        logger.debug("stype: %s", stype)

        host = settings.FTPD_HOST
        port = settings.FTPD_PORT
        rootdir = settings.FTPD_ROOT
        ftp_server = NotificationFTPServer(host, port, rootdir, stype=stype)
        ftp_server.run()
