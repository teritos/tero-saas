"""Mordor channel consumers."""

import logging

from channels.auth import channel_session_user, channel_session_user_from_http

from alarm import events
from alarm.channels import get_alarm_group
from alarm.models import (
    Alarm,
    AlarmImage
)

LOGGER = logging.getLogger('mordor')


@channel_session_user_from_http
def ws_auth(message):
    """Add user to its group alarm."""
    if not message.user or message.user.is_anonymous:
        LOGGER.debug('Invalid user %s', message.user)
        return
    group = get_alarm_group(message.user)
    group.add(message.reply_channel)
    LOGGER.debug('User %s added to group %s', message.user, group.name)


# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message):
    """When user disconnects, remove its group name."""
    group = get_alarm_group(message.user)
    group.discard(message.reply_channel)
    LOGGER.debug('User %s removed from %s', message.user, group.name)


def ws_echo(message):
    """Echo WSGI messages."""
    message.reply_channel.send({
        "text": message.content['text'],
    })


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
