from django.core.management.base import BaseCommand
from bot.telegram import main


class Command(BaseCommand):
    help = 'Run Kaia bot'

    def handle(self, *args, **options):
        main()
