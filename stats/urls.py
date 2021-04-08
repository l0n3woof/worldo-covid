from django.urls import path

from .views import *

urlpatterns = [
        path("stats/", GetStats.as_view())
        ]
