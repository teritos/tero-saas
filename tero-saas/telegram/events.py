"""Telegram event listeners."""

from alarm.events import MOTION_DETECTED
from telegram.api import send_image
import logging
import base64
import io


logger = logging.getLogger('telegram')


def watch_received_images(*args, **kwargs):
    username = kwargs.get('username')
    sender = kwargs.get('sender')
    encoded_image = kwargs.get('encoded_image')
    b_image = io.BytesIO(base64.b64decode(encoded_image))
    send_image(username, b_image)
    logger.debug('Sent image to %s with origin %s', username, sender)


def setup_events(observable):
    events = observable.events[MOTION_DETECTED]
    events.handlers.add(watch_received_images)
