"""Dashboard urls."""

from django.conf.urls import url
from .views import (
    Register,
    Login,
    Logout,
    ajax_login
)


# pylint: disable=C0103
urlpatterns = [
    url(r'^register$', Register.as_view(), name='register'),
    url(r'^login$', Login.as_view(), name='login'),
    url(r'^logout$', Logout.as_view(), name='logout'),
    url(r'^ajax-login/$', ajax_login, name='ajax_login'),
]
