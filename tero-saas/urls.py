from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from alarm.views import save_image


urlpatterns = [
    url(r'^telegram/', include('apps.telegram.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^images/upload', save_image)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
