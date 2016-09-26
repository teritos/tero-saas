from django.contrib.auth.models import User
from django.db import models
from core import signals
import os


class Alarm(models.Model):
    """An alarm """

    active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def activate(self):
        self.active = True
        self.save()

    def deactivate(self):
        self.active = False
        self.save()

    def motion_detected(self, filepath=None):
        signals.motion_detected.send(sender=self.__class__, active=self.active)

    def __str__(self):
        return "{} - {}".format(self.id, self.active)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alarm = models.ForeignKey(Alarm)

    @classmethod
    def create(cls, username, password, alarm=None, ftpd=False, **kwargs):
        """Create a basic user.

        Arguments:
            username(bytes):        username
            passowrd:               password
            alarm;                  AlarmProfile instance
            ftpd:                   Set to True if you want to create an FTP account
                                    for this user.
        """
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        if ftpd:
            from ftpd.models import FTPUser
            if not FTPUser.objects.filter(user=user).exists():
                FTPUser.objects.create(user=user)

        if alarm is None:
            alarm = Alarm.objects.create()

        user_profile = cls.objects.create(user=user, alarm=alarm)

        return user_profile


    def __str__(self):
        return "{}".format(self.user)
