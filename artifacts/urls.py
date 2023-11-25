__author__ = "reed@reedjones.me"
from django.urls import path
from . import api
from .admin import admin_site


urlpatterns = [
    path('custom_admin/', admin_site.urls),

    path('locations/', api.StateList.as_view(), name='location-list'),
    path('locations/<int:pk>/', api.StateDetail.as_view(), name='location-detail'),
    # Add URLs for other views...
]