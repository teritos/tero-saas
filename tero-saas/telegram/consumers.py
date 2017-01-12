"""Telegram channel consumer."""
from alarm.events import observable
from telegram.api import send_message
from telegram.events import setup_events


setup_events(observable)


def telegram_consumer(message):
    """Consume messages queued into messengers.telegram."""
    text = message['text']
    username = message['username']
    filepath = message['filepath']
    send_message(username, text, filepath)
