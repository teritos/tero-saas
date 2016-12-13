import os 
from django.contrib.auth.models import User
from django.db import models

from ftpd.models import FTPAccount


class Alarm(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='alarm_members')
    active = models.BooleanField(default=False)
    joined = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, username, password):
        """Create a new alarm."""
        alarm = cls()
        alarm.owner = User.objects.create_user(username, password=password) 
        alarm.save()

        ftp_account = FTPAccount(alarm=alarm)
        ftp_account.save()

        return alarm

    @classmethod
    def is_active_for(cls, username):
        return cls.objects.values('active').get(owner__username=username).get('active')

    @classmethod
    def get_by_username(cls, username):
        return cls.objects.get(owner__username=username)

    def activate(self):
        self.active = True
        self.save()

    def deactivate(self):
        self.active = False
        self.save()

    @staticmethod
    def images_upload_path(instance, filename):
        path = "{}/{}".format(instance.alarm.pk, filename)
        return os.path.join(instance.UPLOAD_TO, path)

    def __str__(self):
        return "{} {}".format(self.owner, self.active)


class AlarmImage(models.Model):
    UPLOAD_TO = 'alarm-images'

    alarm = models.ForeignKey(Alarm, related_name='images')
    image = models.ImageField(upload_to=Alarm.images_upload_path)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.url
