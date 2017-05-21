"""Vision consumers."""

import logging

from alarm import events
from alarm.models import (
    Alarm,
    AlarmImage
)

LOGGER = logging.getLogger('vision')


def handle_image(payload):
    """Handle images."""
    encoded_image = payload['encoded_image']
    filetype = payload['filetype']
    username = payload['username']
    sender = payload['sender']
    LOGGER.debug('Received image from %s', sender)

    alarm = Alarm.get_by_username(username)
    alarm_image = AlarmImage.create_from_encoded_data(encoded_image, filetype, alarm)
    print('ALARM IMAGE URL %s' % alarm_image.full_url)

    if alarm.active:
        Alarm.notify(
            Event=events.MotionDetected,
            sender=sender,
            username=username,
            filetype=filetype,
            image_url=alarm_image.full_url,
        )
