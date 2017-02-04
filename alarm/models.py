"""Alarm models."""

import os
import logging
from django.contrib.auth.models import User
from django.db import models


LOGGER = logging.getLogger('mordor')


class Alarm(models.Model):
    """A user alarm."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alarms')
    members = models.ManyToManyField(User, related_name='alarm_members')
    active = models.BooleanField(default=False)
    joined = models.DateField(auto_now_add=True)
    label = models.CharField(max_length=150, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, username, password):
        """Create a new alarm."""
        alarm = cls()
        user, created = User.objects.get_or_create(username=username)
        if created is True:
            user.set_password(password)
            user.save()
        alarm.owner = user
        alarm.save()

        return alarm

    @classmethod
    def is_active_for(cls, username):
        """Return if alarm is active for given username."""
        # pylint: disable=no-member
        return cls.objects.values('active').get(owner__username=username).get('active')

    @classmethod
    def get_by_username(cls, username):
        """Return alarm for given username."""
        # pylint: disable=no-member
        return cls.objects.get(owner__username=username)

    @classmethod
    def notify(cls, event_type, *args, **kwargs):
        """TODO: Implement"""

    def activate(self):
        """Set alarm as active."""
        self.active = True
        self.save()

    def deactivate(self):
        """Set alarm as inactive."""
        self.active = False
        self.save()

    @staticmethod
    def images_upload_path(instance, filename):
        """Returns path to where upload images for this alarm."""
        path = "{}/{}".format(instance.alarm.pk, filename)
        return os.path.join(instance.UPLOAD_TO, path)

    def save(self, *args, **kwargs):
        if not self.label:
            self.label = "alarm-{}".format(self.owner.username)
        super(Alarm, self).save(*args, **kwargs)

    def __str__(self):
        return "{} {}".format(self.owner, self.active)


class AlarmImage(models.Model):
    """An image for an alarm"""
    UPLOAD_TO = 'alarm-images'

    alarm = models.ForeignKey(Alarm, related_name='images')
    image = models.ImageField(upload_to=Alarm.images_upload_path)
    timestamp = models.DateTimeField(auto_now_add=True)


class Device(models.Model):
    """A user device (tablet, smartphone, etc.)"""
    user = models.ForeignKey(User, related_name='devices')
    onesignal_id = models.CharField(max_length=50)
    token = models.CharField(max_length=100)

    def __str__(self):
        return self.id  # pylint: disable=E1101
