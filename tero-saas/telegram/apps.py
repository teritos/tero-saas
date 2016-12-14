from django.apps import AppConfig
from django.db.models.signals import post_save


class TelegramConfig(AppConfig):
    name = 'telegram'

    def ready(self):
        from telegram.signals import notify_telegram_user
        post_save.connect(notify_telegram_user, sender='alarm.AlarmImage')
