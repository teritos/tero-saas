from telegram.api import send_message


def telegram_consumer(message):
    text = message['text']
    username = message['username']
    filepath = message['filepath']
    send_message(username, text, filepath)
