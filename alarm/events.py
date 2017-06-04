"""Alarm Event names"""

import logging
import zope.event.classhandler
from base64 import b64decode
from vendors import onesignal
from vision.cloud import azure
from alarm.models import AlarmImage
from django.contrib.auth.models import User


logger = logging.getLogger('alarm')  # pylint: disable=C0103


class Event(object):
    """An alarm event."""
    @classmethod
    def GetEventInstanceFromKwargs(cls, **kwargs):  # pylint: disable=C0103
        """Return an event instance with attrs taken from kwargs."""
        event = cls()
        for key, val in kwargs.items():
            setattr(event, key, val)
        return event


class MotionDetected(Event):
    """Trigger this when motion is detected."""


@zope.event.classhandler.handler(MotionDetected)
def handle_motion_detection(event):
    """Handle motion detection."""
    # Save image on DB
    image = AlarmImage.create_from_encoded_data(event.image64, event.filetype, event.alarm)

    # Notify using OneSignal API
    message = 'Movimiento detectado'

    # If human detection is enabled, check it
    if event.alarm.human_detection:
        tag_list = azure.find_humans_on(b64decode(event.image64))
        print(tag_list)
        if tag_list:
            message = 'Intrusos detectados!!!'
    print(message)
    user = User.objects.get(username=event.username)
    logger.debug('%s en Alarma %s', message, event.alarm)
    onesignal.send_message(user, message, title='Tero [{}]'.format(event.sender), big_picture=image.full_url)
