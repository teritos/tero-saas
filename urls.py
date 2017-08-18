"""General project urls."""

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


# pylint: disable=C0103
urlpatterns = [
    url(r'^api/', include('alarm.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^members/', include('dashboard.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
