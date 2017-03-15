"""OneSignal API."""

import json
import logging
import requests
from django.conf import settings


logger = logging.getLogger('onesignal')  # pylint: disable=C0103


def send_message(user, message, title=''):
    """Envia un mensaje de chat un dispositivo."""

    header = {'Content-Type': 'application/json; charset=utf-8',
              'Authorization': 'Basic ' + settings.ONE_SIGNAL_TOKEN}

    payload = {
        'app_id': settings.ONE_SIGNAL_APP_ID,
        'include_player_ids': [device.onesignal_id for device in user.devices.all()],
        'android_group': '3040',
        'contents': {
            'en': message,
            'es': message,
        },
        'headings': {
            'en': title,
            'es': title,
        },
    }

    logger.debug('Sending onesignal notification to user %s', user)
    response = requests.post(
        'https://onesignal.com/api/v1/notifications',
        headers=header,
        data=json.dumps(payload)
        )
    logger.debug('Response was %s %s', response.status_code, response.reason)
