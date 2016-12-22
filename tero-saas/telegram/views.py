from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.views import View
from telegram.models import TelegramUser

import requests
import json


TOKEN = settings.TELEGRAM_BOT_TOKEN
BASE_URL = settings.TELEGRAM_API_URL


class GetMeView(View):
    """GetMe View."""

    def get(self, request):
        url = BASE_URL + 'getMe'
        response = requests.get(url)
        return JsonResponse(data=response.json())


class ResetWebhookView(View):
    """Reset configured webhook."""

    def get(self, request):
        url = ''.join((BASE_URL, 'setWebhook?url=""'))
        response = requests.get(url)
        return JsonResponse(data=response.json())


class SetWebhookView(View):
    """Configure a webhook url."""

    def get(self, request):
        webhook_url = request.GET.get('url')
        url = ''.join((BASE_URL, 'setWebhook?url={}'.format(webhook_url)))
        response = requests.get(url)
        return JsonResponse(data=response.json())


class WebhookInfoView(View):
    """Returns information from configured webhook."""

    def get(self, request):
        url = ''.join((BASE_URL, 'getWebhookInfo'))
        response = requests.get(url)
        return JsonResponse(data=response.json())


class WebhookView(View):
    """Webhook View that recieves telegram messages."""

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(WebhookView, self).dispatch(*args, **kwargs)

    def get_user_by_chatid(self, chatid):
        return TelegramUser.objects.values('user').get(chat_id=chatid)['user']

    def handle_message(self, message):
        chatid = message['chat']['id']
        message_id = message['message_id']
        user = self.get_user_by_chatid(chatid)
        if message == 'a':
            user.alarm.activate()
            self.send_message(chatid, 'Alarma activada.', reply_to=message_id)
        elif message == 'd':
            user.alarm.deactivate()
            self.send_message(chatid, 'Alarma desactivada.', reply_to=message_id)
        else:
            status = 'Activa' if user.alarm.active else 'Desactivada'
            self.send_message(chatid, 'La alarma se encuentra {}.'.format(status), reply_to=message_id)

    def send_message(self, chatid, message, reply_to):
        payload = {
            'chat_id': chatid,
            'text': message, 
            'disable_web_page_preview': 'true',
            'reply_to_message_id': reply_to,
        }
        url = ''.join((BASE_URL, 'sendMessage'))
        response = requests.get(url, params=payload)
        return response

    def post(self, request):

        if request.content_type != 'application/json':
            return HttpResponseForbidden()

        data = json.loads(request.body.decode('utf-8'))
        message = data['message']
        response = self.handle_message(message)
        return JsonResponse(data=response.json())
