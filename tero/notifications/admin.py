from django.contrib import admin
from notifications.models import NotificationUserProfile
from notifications.telegram.models import TelegramNotificationHandler, TelegramBot

admin.site.register(NotificationUserProfile)

admin.site.register(TelegramBot)
admin.site.register(TelegramNotificationHandler)
