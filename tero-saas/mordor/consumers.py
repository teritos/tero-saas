"""Mordor channel consumers."""

import logging
from mordor.channels import get_alarm_group
from channels.auth import channel_session_user, channel_session_user_from_http


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
