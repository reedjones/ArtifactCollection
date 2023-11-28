__author__ = "reed@reedjones.me"



from django.conf import settings
from DataETL.ETL.DataCleaner import AwMainDataCleaner
from django.core.management.base import BaseCommand
from .loader import AreaLoader, RegionLoader, test_load_value, load_value
import json

class Command(BaseCommand):
    help = "Clears caches"

    def handle(self, **options):
        data = []
        service = AwMainDataCleaner()
        targets = service.model_class.objects.all()
        for target in targets:
            output = {
                'old.pk': target.pk,
                'old.item_number': target.aw_item_number
            }

            output['county'] = target.county
            output['state'] = target.aw_state
            print(f"{output}")
            data.append(output)
        with open('county_state.json', 'w+' ) as f:
            json.dump(data, f)