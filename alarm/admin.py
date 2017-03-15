from django.contrib import admin
from alarm.models import (
    Alarm,
    AlarmImage,
    Device
)


admin.site.register(Alarm)
admin.site.register(AlarmImage)
admin.site.register(Device)
