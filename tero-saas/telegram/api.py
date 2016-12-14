import requests
from django.conf import settings
from telegram.models import TelegramUser


BASE_URL = settings.TELEGRAM_API_URL


def send_message(username, message):

    chat_id = TelegramUser.objects.values('telegram_id').get(user__username=username).get('telegram_id') 
    payload = {
        'chat_id': chat_id,
        'text': message, 
        'disable_web_page_preview': 'true',
    }
    url = ''.join((BASE_URL, 'sendMessage'))
    response = requests.get(url, params=payload)
    print(response.text)
