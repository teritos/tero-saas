"""Alarm models."""

import os
import uuid
import logging
import zope.event
from datetime import datetime
from base64 import b64decode
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.conf import settings
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
    def notify(cls, Event, *args, **kwargs):
        """Trigger an event."""
        event = Event.GetEventInstanceFromKwargs(**kwargs)
        zope.event.notify(event)

    @staticmethod
    def images_upload_path(instance, filename):
        """Returns path to where upload images for this alarm."""
        path = "{}/{}".format(instance.alarm.pk, filename)
        return os.path.join(instance.UPLOAD_TO, path)

    def activate(self):
        """Set alarm as active."""
        self.active = True
        self.save()

    def deactivate(self):
        """Set alarm as inactive."""
        self.active = False
        self.save()

    def save(self, *args, **kwargs):
        if not self.label:
            self.label = "alarm-{}".format(self.owner.username)
        super(Alarm, self).save(*args, **kwargs)

    def __str__(self):
        return "{} {}".format(self.owner, self.active)


def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/alarm-images-<id>/<filename>
    return 'alarm-images-{0}/{1}'.format(instance.alarm.id, filename)


class AlarmImage(models.Model):
    """An image for an alarm"""
    image = models.ImageField(upload_to=image_directory_path)
    alarm = models.ForeignKey(Alarm, related_name='images')
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def full_url(self):
        """Return AlarmImage full url."""
        domain = settings.FULL_DOMAIN
        url = ''.join((domain, self.image.url))
        return url

    @staticmethod
    def get_file_name(alarm, filetype):
        """Returns a unique filename.
        :param alarm    Alarm instance. 
        """
        uid = uuid.uuid4()
        date = datetime.now().strftime("%d%H%m%S")
        if not filetype.startswith('.'):
            filetype = ''.join(('.', filetype))
        name = "{}-{}-{}{}".format(alarm.id, date, uid, filetype)
        return name

    @classmethod
    def create_from_encoded_data(cls, data, filetype, alarm):
        """Create and return an AlarmImage instance from given data."""
        # b64data = b64decode(data).split('base64', 1)
        b64data = b64decode(data)
        image_name = AlarmImage.get_file_name(alarm, filetype)
        alarm_image = cls()
        alarm_image.alarm = alarm
        alarm_image.save(name=image_name, content=ContentFile(b64data))
        return alarm_image

    def __str__(self):
        return "{}".format(self.image.name)


class Device(models.Model):
    """A user device (tablet, smartphone, etc.)"""
    user = models.ForeignKey(User, related_name='devices')
    onesignal_id = models.CharField(max_length=50)
    token = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)  # pylint: disable=E1101
