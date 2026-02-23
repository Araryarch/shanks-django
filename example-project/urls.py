"""URL Configuration"""

from app.routes import urlpatterns as api_urls
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(api_urls)),
]
