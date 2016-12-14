from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.views import View

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

    def post(self, request):

        if request.content_type != 'application/json':
            return HttpResponseForbidden()

        data = json.loads(request.body.decode('utf-8'))
        message = data['message']
        message_id = message['message_id']
        message_text = message['text']
        from_ = message['from']
        from_id = from_['id']
        chat = message['chat']
        chat_id = chat['id']
        print(chat_id)
        chat_type = chat['type']
        chat_first_name = chat['first_name']

        payload = {
            'chat_id': chat_id,
            'text': message_text, 
            'disable_web_page_preview': 'true',
            'reply_to_message_id': message_id,
        }
        url = ''.join((BASE_URL, 'sendMessage'))
        response = requests.get(url, params=payload)

        return JsonResponse(data=response.json())
