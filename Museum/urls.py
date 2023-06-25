from django.urls import path
from Museum.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', main, name='main'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('exhibits/<int:pk>', exhibits, name='exhibits'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)