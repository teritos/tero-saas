from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from core.models import UserProfile


class Command(BaseCommand):

    def handle(self, *args, **options):
        for userprofile in UserProfile.objects.all():
            print('UserProfile [{}]\tAlarm id: [{} - active: {}].'.format(
                userprofile, userprofile.alarm.id, userprofile.alarm.active))
