from django.db import models
from django.contrib.auth.models import User


class FTPUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    homedir = models.CharField(max_length=255)
    permissions = models.CharField(max_length=20, default='elradfmwM')
