"""Alarm Event names"""

import logging
import zope.event.classhandler
from vendors import onesignal
from django.contrib.auth.models import User


logger = logging.getLogger('alarm')  # pylint: disable=C0103


class Event(object):
    """An alarm event."""
    @classmethod
    def GetEventInstanceFromKwargs(cls, **kwargs):  # pylint: disable=C0103
        """Return an event instance with attrs taken from kwargs."""
        event = cls()
        for key, val in kwargs:
            setattr(event, key, val)
        return event


class MotionDetected(Event):
    """Trigger this when motion is detected."""


@zope.event.classhandler.handler(MotionDetected)
def send_onesignal_notification(event):
    """Notify users using onesignal."""
    user = User.objects.get(username=event.username)
    message = 'Movimiento detectado.'
    onesignal.send_message(user, message, title='Tero.')
