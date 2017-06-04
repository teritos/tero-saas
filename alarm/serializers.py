"""Serializers for Alarm API."""

from rest_framework import serializers
from alarm.models import (
    Alarm,
    AlarmImage,
    Device,
)


class AlarmSerializer(serializers.ModelSerializer):
    """User Alarm Serializer."""
    class Meta:  # pylint: disable=C0111,R0903
        model = Alarm
        fields = ('id', 'owner', 'active', 'label')


class AlarmImageSerializer(serializers.ModelSerializer):
    """AlarmImage Serializer."""
    class Meta:  # pylint: disable=C0111,R0903
        model = AlarmImage
        fields = ('id', 'alarm', 'image', 'full_url')


class DeviceSerializer(serializers.ModelSerializer):
    """User Device Serializer."""
    class Meta:  # pylint: disable=C0111,R0903
        model = Device
        fields = ('id', 'user', 'onesignal_id', 'token')
