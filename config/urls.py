"""
Root URL configuration for the Jholo University project.

Kept intentionally thin. Each app owns its own routes and exposes them under
a namespace, so templates reference {% url 'core:home' %} or
{% url 'notice:notice_detail' notice.slug %} rather than hardcoded paths.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('core.urls')),
    path('notice/', include('notice.urls')),
]

# Dev-only: Django serves these itself. In production, WhiteNoise handles
# static/ and uploaded media belongs in object storage or a CDN.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
