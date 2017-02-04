"""Serializers for Alarm API."""

from rest_framework import serializers
from alarm.models import (
    Alarm,
    Device,
)


class AlarmSerializer(serializers.ModelSerializer):
    """User Alarm Serializer."""
    class Meta:  # pylint: disable=C0111,R0903
        model = Alarm
        fields = ('id', 'owner', 'active', 'label')


class DeviceSerializer(serializers.ModelSerializer):
    """User Device Serializer."""
    class Meta:  # pylint: disable=C0111,R0903
        model = Device
        fields = ('id', 'user', 'onesignal_id', 'token')
