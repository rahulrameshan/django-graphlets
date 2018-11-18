"""
URL patterns for testing app.
"""
from django.conf.urls import url

from . import views

app_name = 'tests'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
