__author__ = "reed@reedjones.me"
from django.urls import path
from . import api

urlpatterns = [
    path('locations/', api.StateList.as_view(), name='location-list'),
    path('locations/<int:pk>/', api.StateDetail.as_view(), name='location-detail'),
    # Add URLs for other views...
]