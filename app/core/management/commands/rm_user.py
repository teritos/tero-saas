from django.core.management.base import BaseCommand, CommandError
from core.models import UserProfile


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('-u', '--username', required=True)

    def handle(self, *args, **options):
        username = options['username']
        if not UserProfile.objects.filter(user__username=username).exists():
            print('User [{}] does not exists'.format(username))
            return
        UserProfile.objects.filter(user__username=username).delete()
        print('User [{}] was removed!'.format(username))
