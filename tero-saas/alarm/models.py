from django.contrib.auth.models import User
from ftpd.models import FTPAccount
from django.db import models


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
        alarm.user = User.objects.create_user(username, password) 
        alarm.save()

        ftp_account = FTPAccount(alarm=alarm)
        ftp_account.save()

        return alarm

    def activate(self):
        self.active = True
        self.save()

    def deactivate(self):
        self.active = False
        self.save()

    def __str__(self):
        return "{} {}".format(self.owner, self.active)

