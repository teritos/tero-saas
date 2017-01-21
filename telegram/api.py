import logging
import requests
from django.conf import settings
from telegram.models import TelegramUser


BASE_URL = settings.TELEGRAM_API_URL
TELEGRAM_BOT_TOKEN = '265716638:AAGqJxPa2jnzRh-NAdSOgXxZYoaNnL0Z2aM'
BASE_URL = 'https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/'
logger = logging.getLogger('telegram')  # pylint: disable=invalid-name


def send_message(username, message, filepath):
    """Send a message to a telegram user."""
    logger.debug('TO DEPRECATE: telegram.api.send_message')

    # pylint: disable=no-member
    chat_id = TelegramUser.objects.values('telegram_id').get(
        user__username=username).get('telegram_id')
    payload = {
        'chat_id': chat_id,
        'text': message,
        'disable_web_page_preview': 'true',
    }
    url = ''.join((BASE_URL, 'sendMessage'))
    print(url)
    requests.get(url, params=payload)

    url = ''.join((BASE_URL, 'sendPhoto'))
    files = {'photo': open(filepath, 'rb')}
    requests.post(url, params=payload, files=files)



def send_text(username, text):
    """Send a text to a user.

        Arguments:
            username        Username
            text            Message to send
    """
    # pylint: disable=no-member
    chat_id = TelegramUser.objects.values('telegram_id').get(
        user__username=username).get('telegram_id')

    payload = {
        'chat_id': chat_id,
        'text': text,
        'disable_web_page_preview': 'true',
    }
    url = ''.join((BASE_URL, 'sendMessage'))
    requests.get(url, params=payload)


def send_image(username, img_bytes):
    """Send an image to a user.

        Arguments:
            username        Username
            imagepath       Path to image
    """
    # pylint: disable=no-member
    chat_id = TelegramUser.objects.values('telegram_id').get(
        user__username=username).get('telegram_id')

    payload = {
        'chat_id': chat_id,
        'disable_web_page_preview': 'true',
    }
    files = {'photo': img_bytes}
    url = ''.join((BASE_URL, 'sendPhoto'))
    response = requests.post(url, params=payload, files=files)
    logger.debug(response.status_code)
    logger.debug(response.text)

