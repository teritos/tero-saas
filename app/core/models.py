from django.db import models
from django.contrib.auth.models import User
import telegram
import os


class TelegramProfile(models.Model):
    bot_token = models.CharField(max_length=255)
    chat_id = models.CharField(max_length=255)
    # name = models.CharField(max_length=255)

    @property
    def bot(self):
        """Return a telegram bot instance."""
        return telegram.Bot(token=self.bot_token)

    def send_message(self, message):
        self.bot.sendMessage(chat_id=self.chat_id, text=message)

    def send_photo(self, path):
        self.bot.sendPhoto(chat_id=self.chat_id, photo=open(path, 'rb'))

    def __str__(self):
        return "{}".format(self.chat_id)


class AlarmProfile(models.Model):
    active = models.BooleanField(default=False)
    name = models.CharField(max_length=80, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def activate(self):
        self.active = True
        self.save()

    def deactivate(self):
        self.active = False
        self.save()

    def notify_motion_detected(self, file):
        msg = "Movimiento detectado!"
        if self.active:
            # Get all user profiles that should be notified
            users_to_notify = self.get_users_to_notify()
            for user_profile in users_to_notify:
                if user_profile.has_telegram:
                    user_profile.telegram.send_message(msg)
                    user_profile.telegram.send_photo(file)
        else:
            # Keep hard drive space
            os.remove(file)

    def get_users_to_notify(self):
        """Return a list of user profiles that should be notified"""
        return UserProfile.objects.filter(alarm=self).all()

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = str(self.id)

        super(AlarmProfile, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.name or self.id, self.active)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alarm = models.ForeignKey(AlarmProfile)
    telegram = models.OneToOneField(
        TelegramProfile,
        null=True,
        blank=True,
        on_delete=models.CASCADE
        )

    @classmethod
    def create(cls, username, password, alarm=None, ftpd=False, **kwargs):
        """Create a basic user.

        Arguments:
            username(bytes):        username
            passowrd:               password
            alarm;                  AlarmProfile instance
            ftpd:                   Set to True if you want to create an FTP account
                                    for this user.

        Keyword Arguments:
            telegram_token:         Your telegram account ID
            telegram_chat_id:       Your telegram BOT id.
                                    If telegram_token and telegram_chat_id are
                                    defined, Tero creates a TelegramProfile for
                                    this user.
        """
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        if ftpd:
            from ftpd.models import FTPUser
            if not FTPUser.objects.filter(user=user).exists():
                FTPUser.objects.create(user=user)

        alarm, created = AlarmProfile.objects.get_or_create(name=alarm)

        telegram_token = kwargs.get('telegram_token')
        telegram_chat_id = kwargs.get('telegram_chat_id')
        bot = None
        if telegram_token and telegram_chat_id:
            bot = TelegramProfile.objects.create(
                bot_token=telegram_token,
                chat_id=telegram_chat_id)

        user_profile = cls.objects.create(
            user=user,
            alarm=alarm,
            telegram=bot
        )

        return user_profile

    @property
    def has_telegram(self):
        return self.telegram

    def __str__(self):
        return "{}".format(self.user)
