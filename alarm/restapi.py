"""REST API for Alarm."""

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from alarm.serializers import (
    AlarmSerializer,
    AlarmImageSerializer,
    DeviceSerializer,
)
from alarm.models import (
    Alarm,
    AlarmImage,
    Device,
)


version = 'v1'  # pylint: disable=C0103


class AlarmListView(APIView):
    """List alarms from a user."""
    authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    url = "%s/alarm/$" % version

    def get(self, request):  # pylint: disable=C0103,R0201,W0613
        """Get an alarm by its pk."""
        if request.user.is_superuser:
            alarm_list = Alarm.objects.all().order_by('id')  # pylint: disable=E1101
        else:
            alarm_list = Alarm.objects.filter(owner=request.user).all().order_by('id')  # pylint: disable=E1101
        serialized = AlarmSerializer(alarm_list, many=True)
        return Response(serialized.data)


class AlarmImageView(APIView):
    """API for an alarm image."""
    authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    url = "%s/alarm/images$" % version

    def get(self, request):  # pylint: disable=C0103,R0201,W0613
        """Get alarm images"""

        alarms = AlarmImage.objects.filter()
        serialized = AlarmImageSerializer(alarms, many=True)
        return Response(serialized.data)

    def list(self, request):  # pylint: disable=C0103,R0201,W0613
        """Get alarm images"""

        alarms = AlarmImage.objects.filter()
        serialized = AlarmImageSerializer(alarms, many=True)
        return Response(serialized.data)


class AlarmView(APIView):
    """API for an alarm."""
    authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    url = "%s/alarm/(?P<pk>[0-9]+)$" % version

    def get(self, request, pk):  # pylint: disable=C0103,R0201,W0613
        """Get an alarm by its pk."""
        if request.user.is_superuser:
            alarm = get_object_or_404(Alarm, pk=pk)
        else:
            alarm = get_object_or_404(Alarm, pk=pk, owner=request.user)
        serialized = AlarmSerializer(alarm)
        return Response(serialized.data)

    def put(self, request, pk):  # pylint: disable=C0103,R0201,W0613
        """Update an alarm by its pk."""
        if request.user.is_superuser:
            alarm = get_object_or_404(Alarm, pk=pk)
        else:
            alarm = get_object_or_404(Alarm, pk=pk, owner=request.user)

        if request.data.get('status'):
            alarm.activate()
        else:
            alarm.deactivate()

        serialized = AlarmSerializer(alarm)
        return Response(serialized.data)


class DeviceListView(APIView):
    """List devices from a user."""
    authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    url = "%s/device/" % version

    def get(self, request):  # pylint: disable=C0103,R0201,W0613
        """Get a device list by its pk."""
        if request.user.is_superuser:
            device_list = Device.objects.all()  # pylint: disable=E1101
        else:
            device_list = Device.objects.filter(user=request.user).all()  # pylint: disable=E1101
        serialized = DeviceSerializer(device_list, many=True)
        return Response(serialized.data)


class DeviceView(APIView):
    """API for a device."""

    authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    url = "%s/device/(?P<pk>[0-9a-zA-z\-]+)" % version

    def get(self, request, pk):  # pylint: disable=C0103,R0201,W0613
        """Update or create a device by its pk."""
        if request.user.is_superuser:
            device = get_object_or_404(Device, onesignal_id=pk)
        else:
            device, _ = Device.objects.get_or_create(onesignal_id=pk, user=request.user)  # pylint: disable=E1101

        device.save()
        raise Exception('Puto toma!')

        serialized = DeviceSerializer(device)
        return Response(serialized.data)

    def put(self, request, pk):  # pylint: disable=C0103,R0201,W0613
        """Update or create a device by its pk."""

        device, _ = Device.objects.get_or_create(onesignal_id=pk, user=request.user)  # pylint: disable=E1101

        #for key, val in request.data:
        #    setattr(device, key, val)
        device.save()
        raise Exception('Puto toma! put')

        serialized = DeviceSerializer(device)
        return Response(serialized.data)
