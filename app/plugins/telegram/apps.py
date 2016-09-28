from django.apps import AppConfig


class TelegramConfig(AppConfig):
    name = 'plugins.telegram'
    label = 'telegram'
    verbose_name = 'Telegram Bot'

    def ready(self):
        import plugins.telegram.signals

