__author__ = "reed@reedjones.me"

__author__ = "reed@reedjones.me"

from django.conf import settings

from django.core.management.base import BaseCommand
import json

import spacy

from DataETL.ETL.DataCleaner import AwMainDataCleaner

# Load the language model
nlp = spacy.load("en_core_web_sm")


def ok(v):
    return v is not None and str(v).strip() != ''

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
            if ok(target.finder):
                output['finder'] = service.clean_weird(target.finder)
            if ok(target.previous_collections):
                output['previous_collections'] = service.clean_weird(target.previous_collections)
            print(output)
            data.append(output)

        with open('finder_owners.json', 'w+' ) as f:
            json.dump(data, f)