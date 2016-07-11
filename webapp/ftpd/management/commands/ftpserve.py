from django.core.management.base import BaseCommand
from ftpd import main


class Command(BaseCommand):
    help = 'Run ftpd server'

    def handle(self, *args, **options):
        main()
