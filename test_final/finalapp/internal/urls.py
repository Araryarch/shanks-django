"""Main URL Configuration"""
from django.urls import path, include

urlpatterns = [
    path('', include('internal.views')),
    path('', include('internal.routes')),
]
