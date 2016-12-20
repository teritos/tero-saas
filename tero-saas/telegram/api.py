import requests
from django.conf import settings
from telegram.models import TelegramUser


BASE_URL = settings.TELEGRAM_API_URL


def send_message(username, message, filepath):
    """Send a message to a telegram user."""

    chat_id = TelegramUser.objects.values('telegram_id').get(
        user__username=username).get('telegram_id')
    payload = {
        'chat_id': chat_id,
        'text': message,
        'disable_web_page_preview': 'true',
    }
    url = ''.join((BASE_URL, 'sendMessage'))
    requests.get(url, params=payload)

    url = ''.join((BASE_URL, 'sendPhoto'))
    files = {'photo': open(filepath, 'rb')}
    requests.post(url, params=payload, files=files)
