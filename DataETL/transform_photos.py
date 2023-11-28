__author__ = "reed@reedjones.me"

__author__ = "reed@reedjones.me"

from django.conf import settings
from DataETL.ETL.DataCleaner import AwMainDataCleaner
from django.core.management.base import BaseCommand
from .loader import AreaLoader, RegionLoader, test_load_value, load_value
import json

class Command(BaseCommand):
    help = "Clears caches"

    def handle(self, **options):
        photos = [f"photo{i}" for i in range(1, 10)]

        data = []
        service = AwMainDataCleaner()
        targets = service.model_class.objects.all()
        for target in targets:
            output = {
                'old.pk': target.pk,
                'old.item_number': target.aw_item_number
            }
            for item in photos:
                output[item] = getattr(target, item)
            data.append(output)


        with open('photos.json', 'w+' ) as f:
            json.dump(data, f)