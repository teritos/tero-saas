from django.db import models


class Telegram(models.Model):
    pin = models.CharField(max_length=10)
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.pin