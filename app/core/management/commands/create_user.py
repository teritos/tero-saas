from django.core.management.base import BaseCommand, CommandError
from core.models import UserProfile


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('-u', '--username', required=True)
        parser.add_argument('-p', '--password', required=True)

        # Named (optional) arguments
        parser.add_argument(
            '--ftp-user',
            action='store_true',
            dest='ftpd',
            default=False,
            help='Create an ftp account for this user',
        )
        parser.add_argument(
            '--telegram-id',
            action='store',
            dest='telegram_token',
            default=None,
            help='Telegram User ID',
        )

        parser.add_argument(
            '--telegram-bot-id',
            action='store',
            dest='telegram_bot_id',
            default=None,
            help='Telegram BOT ID',
        )


    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        ftpd=False
        telegram_token = options['telegram_token']
        telegram_chat_id = options['telegram_bot_id']
        if UserProfile.objects.filter(user__username=username).exists():
            print('User [{}] already exists,'
                  ' please choose another username.\n'.format(username))
            return
        user_profile = UserProfile.create(
            username=username,
            password=password,
            ftpd=ftpd,
            telegram_token=telegram_token,
            telegram_chat_id=telegram_chat_id
        )
        print('User [{}] AlarmProfile [{}] created!\n'.format(
            user_profile.id, user_profile.alarm.id
        ))
