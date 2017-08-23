"""Alarm admin."""
from django.contrib import admin
from alarm.models import (
    Alarm,
    AlarmImage,
    Device
)


class AlarmAdmin(admin.ModelAdmin):
    """Alarm Model Admin."""
    list_display = ('id', 'owner', 'label', 'last_modified', 'active')


admin.site.register(Alarm, AlarmAdmin)
admin.site.register(AlarmImage)
admin.site.register(Device)
