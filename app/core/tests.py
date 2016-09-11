from django.contrib.auth.models import User
from django.test import TestCase
from core.models import (
    TelegramProfile,
    AlarmProfile,
    UserProfile
)


class TestUserProfile(TestCase):

    def setUp(self):
        self.alarm = AlarmProfile.objects.create()
        self.user = User.objects.create(username='test', password='secret')
        self.user2 = User.objects.create(username='test2', password='secret')
        self.user_profile = UserProfile.objects.create(
            user=self.user, alarm=self.alarm
            )
        self.user_profile2 = UserProfile.objects.create(
            user=self.user2, alarm=self.alarm
        )

    def tearDown(self):
        TelegramProfile.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.all().delete()

    def test_user_alarm(self):
        user_profile = self.user_profile
        user_profile2 = self.user_profile2
        self.assertTrue(user_profile.alarm.active == False)
        self.assertTrue(user_profile2.alarm.active == False)

        user_profile.alarm.activate()
        self.assertTrue(user_profile.alarm.active == True)
        self.assertTrue(user_profile2.alarm.active == True)

        user_profile2.alarm.deactivate()
        self.assertTrue(user_profile.alarm.active == False)
        self.assertTrue(user_profile2.alarm.active == False)

    def test_user_telegram_bot(self):
        user_profile = self.user_profile
        self.assertTrue(user_profile.telegram == None)

        bot = TelegramProfile.objects.create(bot_token='xxx', chat_id='secret')
        user_profile.telegram = bot
        user_profile.save()
        self.assertTrue(user_profile.telegram == bot)

    def test_create_user_profile(self):
        user_profile = UserProfile.create(
            username='emi',
            password='secret',
            fptd=False,
        )

        user = User.objects.get(username='emi')
        self.assertEquals(user_profile.user, user)
        self.assertTrue(user_profile.alarm.active == False)

    def test_create_telegram_profile(self):
        user_profile = UserProfile.create(
            username='emi',
            password='secret',
            fptd=False,
            telegram_token='xxx',
            telegram_chat_id='xxx'
        )
        self.assertEquals(
            TelegramProfile.objects.filter(bot_token='xxx').first(),
            user_profile.telegram
        )
