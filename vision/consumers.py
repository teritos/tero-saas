"""Vision consumers."""

import logging

from base64 import b64decode
from alarm import events
from alarm.models import (
    Alarm,
    AlarmImage
)
from vision.cloud import azure

logger = logging.getLogger('vision')


def handle_image(payload):
    """Handle images."""
    encoded_image = payload['encoded_image']
    filetype = payload['filetype']
    username = payload['username']
    sender = payload['sender']
    logger.debug('Received image from %s', sender)

    alarm = Alarm.get_by_username(username)
    alarm_image = AlarmImage.create_from_encoded_data(encoded_image, filetype, alarm)

    if alarm.active:
        Alarm.notify(
            Event=events.MotionDetected,
            sender=sender,
            username=username,
            filetype=filetype,
            image_url=alarm_image.full_url,
        )


def get_image_tags(payload):
    """Return tags from given image."""
    encoded_image = payload['encoded_image']  # encoded in base64
    image = b64decode(encoded_image)
    tags = azure.get_image_tags(image)
    return tags
