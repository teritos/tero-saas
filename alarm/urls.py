"""Alarm urls."""

from django.conf.urls import url
from alarm import restapi


# pylint: disable=C0103
urlpatterns = [
    url(r'^%s' % restapi.AlarmView.url, restapi.AlarmView.as_view(), name='rest-alarm'),
    url(r'^%s' % restapi.AlarmListView.url, restapi.AlarmListView.as_view(), name='rest-alarm-list'), # pylint: disable=C0301
]
