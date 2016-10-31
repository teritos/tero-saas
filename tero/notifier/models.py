from django.db import models


class Telegram(models.Model):
    pin = models.CharField(max_length=20)

    def __str__(self):
        return self.pin