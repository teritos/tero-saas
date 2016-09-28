from django.core.management.base import BaseCommand, CommandError
from core.models import UserProfile


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('-u', '--username', required=True)
        parser.add_argument('-p', '--password', required=True)

        parser.add_argument(
            '--alarm',
            action='store',
            dest='alarm',
            default=None,
            help='Alarm name',
        )


    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        ftpd=False
        alarm = options['alarm']

        if UserProfile.objects.filter(user__username=username).exists():
            print('User [{}] already exists,'
                  ' please choose another username.\n'.format(username))
            return

        user_profile = UserProfile.create(
            username=username,
            password=password,
            alarm=alarm,
        )

        print('User [{}] AlarmProfile [{}] created!\n'.format(
            user_profile, user_profile.alarm
        ))
