"""Vision consumers."""

import logging

from base64 import b64decode
from alarm import events
from alarm.models import Alarm
from vision.cloud import azure

logger = logging.getLogger('vision')


def handle_image(payload):
    """Handle images."""
    image64 = payload['encoded_image']  # image encoded in base64
    filetype = payload['filetype']
    username = payload['username']
    sender = payload['sender']
    logger.debug('Received image from %s', sender)

    alarm = Alarm.get_by_username(username)

    if alarm.active:
        Alarm.notify(
            Event=events.MotionDetected,
            alarm=alarm,
            sender=sender,
            username=username,
            filetype=filetype,
            image64=image64,
        )


def get_image_tags(payload):
    """Return tags from given image."""
    encoded_image = payload['encoded_image']  # encoded in base64
    image = b64decode(encoded_image)
    tags = azure.get_image_tags(image)
    return tags
