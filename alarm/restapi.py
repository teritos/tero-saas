"""REST API for Alarm."""

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from alarm.models import Alarm
from alarm.serializers import AlarmSerializer


version = 'v1'  # pylint: disable=C0103


class AlarmView(APIView):
    """API for an alarm."""
    authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    url = "%s/alarm/(?P<pk>[0-9])" % version

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
