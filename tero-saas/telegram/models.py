from django.db import models
from django.contrib.auth.models import User


class TelegramUser(models.Model):
    user = models.OneToOneField(User)
    telegram_id = models.IntegerField()

    def __str__(self):
        return "{} {}".format(self.user, self.telegram_id)
