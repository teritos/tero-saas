from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('-u', '--username', required=True)

    def handle(self, *args, **options):
        username = options['username']
        if not User.objects.filter(username=username).exists():
            print('User [{}] does not exists'.format(username))
            return
        User.objects.filter(username=username).delete()
        print('User [{}] was removed!'.format(username))
