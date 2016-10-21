import logging

from django.db import models
from django.contrib.auth.models import User
from ftpd.models import FTPUser


logger = logging.getLogger(__name__)


class NotificationUserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pin = models.CharField(max_length=10)
    telegram_username = models.CharField(max_length=20)
    telegram_bot_id = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username


class NotificationHandler(models.Model):

    name = models.CharField(max_length=25, unique=True, null=False, blank=False)
    ftp_user = models.ForeignKey(FTPUser)
    active = models.BooleanField(default=True)
    subscribers = models.ManyToManyField(NotificationUserProfile, blank=True)

    def new_notification(self, kwargs=None):
        kwargs = kwargs or {}
        self._handle_new_notification(**kwargs)

    def _handle_new_notification(self):
        raise NotImplementedError("Must be override by subclasses")

    def subscribe(self, nup):
        logger.debug("Subscribing user profile...")
        self.subscribers.add(nup)
        self.save()

    def unsubscribe(self, nup):
        logger.debug("Unsubscribing user profile...")
        self.subscribers.remove(nup)
        self.save()

    class Meta:
        abstract = True
