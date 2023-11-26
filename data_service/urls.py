__author__ = "reed@reedjones.me"
# urls.py
from django.urls import path
from .views import DataServiceAPIView

urlpatterns = [
    path('api/data-service/', DataServiceAPIView.as_view(), name='data-service-api'),
    # Add more paths for other DataService methods if needed
]
