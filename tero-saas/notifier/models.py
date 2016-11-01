from django.db import models
from django.contrib.auth.models import User


class Telegram(models.Model):
    user = models.OneToOneField(User)
    pin = models.CharField(max_length=20)

    def __str__(self):
        return self.pin