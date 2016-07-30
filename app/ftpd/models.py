import os
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth.models import User


class FTPUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    permissions = models.CharField(max_length=20, default='elwm')

    @property
    def homedir(self):
        path = os.path.join(settings.FTPD_ROOT, slugify(self.user))
        if not os.path.isdir(path):
            os.makedirs(path)
        return path

    def __str__(self):
        return "{}".format(self.user)
