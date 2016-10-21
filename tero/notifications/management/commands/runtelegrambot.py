import logging

from django.core.management.base import BaseCommand
from notifications.telegram.telegrambotrunner import TelegramBotRunner


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run A telegram bot registered in this app'

    def add_arguments(self, parser):
        parser.add_argument('-b', '--botname',
                            dest='botname',
                            type=str,
                            help="Telegram botname to run",
                            nargs=1,
                            required=True
                            )

    def handle(self, *args, **options):

        botname = options['botname'].pop()
        logger.info("Running telegram bot %s",  botname)
        TelegramBotRunner.run_telelgram_bot(botname)
