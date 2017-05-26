"""Mordor channel consumers."""

import logging

from channels.auth import channel_session_user, channel_session_user_from_http
from alarm.channels import get_alarm_group

logger = logging.getLogger('alarm')


@channel_session_user_from_http
def ws_auth(message):
    """Add user to its group alarm."""
    if not message.user or message.user.is_anonymous:
        logger.debug('Invalid user %s', message.user)
        return
    group = get_alarm_group(message.user)
    group.add(message.reply_channel)
    logger.debug('User %s added to group %s', message.user, group.name)


# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message):
    """When user disconnects, remove its group name."""
    group = get_alarm_group(message.user)
    group.discard(message.reply_channel)
    logger.debug('User %s removed from %s', message.user, group.name)


def ws_echo(message):
    """Echo WSGI messages."""
    message.reply_channel.send({
        "text": message.content['text'],
    })
