__author__ = "reed@reedjones.me"

from django.urls import path

from . import api
from .admin import admin_site
from .views import StateCountyFilterView

urlpatterns = [
    path('custom_admin/', admin_site.urls),
    path('htmx/state_county_filter/', StateCountyFilterView.as_view(), name='state_county_filter'),


    # Add URLs for other views...
]
