"""
URL configuration for Museum application.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import exhibits, main

app_name = "museum"

urlpatterns = [
    path("", main, name="main"),
    path("exhibits/<int:pk>/", exhibits, name="exhibits"),
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
