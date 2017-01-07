"""Mordor channel consumers."""

from channels import Channel, Group
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
from mordor.channels import get_alarm_group


@channel_session_user_from_http
def ws_auth(message):
    """Add user to its group alarm."""
    if not message.user:
        return
    group = get_alarm_group(message.user)
    group.add(message.reply_channel)

# Connected to websocket.receive
@channel_session_user
def ws_message(message):
    group = get_alarm_group(message.user)
    Group("chat-%s" % message.user.username[0]).send({
        "text": message['text'],
    })

# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message):
    """When user disconnects, remove its group name."""
    group = get_alarm_group(message.user)
    group.discard(message.reply_channel)


def ws_echo(message):
    """Echo WSGI messages."""
    message.reply_channel.send({
        "text": message.content['text'],
    })
