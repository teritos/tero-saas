from django.contrib import admin
from alarm.models import (
    Alarm,
    AlarmImage,
)


admin.site.register(Alarm)
admin.site.register(AlarmImage)
