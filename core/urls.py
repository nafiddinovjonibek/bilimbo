from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from home.media_views import public_media

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, view=public_media, document_root=settings.MEDIA_ROOT)
