__author__ = "reed@reedjones.me"

from django.apps import AppConfig


class DataServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "data_service"
    def ready(self):
        import data_service.signals