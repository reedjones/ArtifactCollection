__author__ = "reed@reedjones.me"

__author__ = "reed@reedjones.me"

from django.conf import settings
from DataETL.ETL.DataCleaner import AwMainDataCleaner
from django.core.management.base import BaseCommand
from .loader import AreaLoader, RegionLoader, test_load_value, load_value, CategoryLoader
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
            output['type'] = target.aw_type
            output['subtype'] = target.aw_subtype
            output['category'] = target.aw_type_category
            cl = CategoryLoader(target)
            output['parsed'] = cl.get_cats_check()
            print(f"{output['parsed']}")
            data.append(output)
        with open('categories.json', 'w+' ) as f:
            json.dump(data, f)