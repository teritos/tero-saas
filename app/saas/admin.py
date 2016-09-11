from django.contrib import admin
from core.models import AlarmProfile, UserProfile, TelegramProfile

admin.site.register(TelegramProfile)
admin.site.register(AlarmProfile)
admin.site.register(UserProfile)
