"""Mordor channel consumers."""


def ws_echo(message):
    """Echo WSGI messages."""
    message.reply_channel.send({
        "text": message.content['text'],
    })
