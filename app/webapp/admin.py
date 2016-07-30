from django.contrib import admin
from webapp.models import AlarmProfile, UserProfile, TelegramProfile

admin.site.register(TelegramProfile)
admin.site.register(AlarmProfile)
admin.site.register(UserProfile)
