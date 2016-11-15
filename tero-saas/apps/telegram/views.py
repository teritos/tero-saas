from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

from django.views import View
import requests


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
        return JsonResponse(data=response.get_json())


class SetWebhookView(View):
    """Configure a webhook url."""

    def get(self, request):
        webhook_url = request.GET.get('url')
        url = ''.join((BASE_URL, 'setWebhook?url=', webhook_url))
        response = requests.get(url)
        return JsonResponse(data=response.get_json())


class WebhookInfoView(View):
    """Returns information from configured webhook."""

    def get(self, request):
        url = ''.join((BASE_URL, 'getWebhookInfo'))
        response = requests.get(url)
        return JsonResponse(data=response.get_json())


class WebhookView(View):
    """Webhook View that recieves telegram messages."""

    def post(self, request):
        import ipdb; ipdb.set_trace()
        data = request.get_json()
        message = data['message']
        from_id = message['from']['id']
        text = message['text']
        message_id = message['message_id']
        chat_id = message['chat']['id']
        msg = 'frulaaaaaaaaaa'
        resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
            'chat_id': str(chat_id),
            'text': msg.encode('utf-8'),
            'disable_web_page_preview': 'true',
            'reply_to_message_id': str(message_id),
        })).read()
        return json.dumps(data)