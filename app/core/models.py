from django.contrib.auth.models import User
from django.db import models
from core import signals
import os


class Alarm(models.Model):
    """An alarm """

    name = models.CharField(max_length=80, null=True, blank=True)
    active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def activate(self):
        self.active = True
        self.save()

    def deactivate(self):
        self.active = False
        self.save()

    def trigger_motion_detected(self, filepath=None):
        signals.motion_detected.send(sender=self.__class__, 
                                     active=self.active,
                                     filepath=filepath)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = str(self.id)

        super(Alarm, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.name or self.id, self.active)


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

        alarm, created = Alarm.objects.get_or_create(name=alarm)

        user_profile = cls.objects.create(
            user=user,
            alarm=alarm,
        )

        signals.userprofile_created.send(
            sender=self.__class__, 
            username=username,
            alarm=alarm,
            ftpd=ftpd
        )

        return user_profile


    def __str__(self):
        return "{}".format(self.user)
