from django.conf.urls import url
from telegram.views import (
    GetMeView,
    ResetWebhookView,
    SetWebhookView,
    WebhookInfoView,
    WebhookView,
)

urlpatterns = [
    url(r'^webhook/get-me', GetMeView.as_view(), name='webhook-get-me'),
    url(r'^webhook/reset', ResetWebhookView.as_view(), name='webhook-reset'),
    url(r'^webhook/set', SetWebhookView.as_view(), name='webhook-set'),
    url(r'^webhook/info', WebhookInfoView.as_view(), name='webhook-info'),
    url(r'^webhook$', WebhookView.as_view(), name='webhook'),
]
