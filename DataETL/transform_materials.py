__author__ = "reed@reedjones.me"

from django.core.management.base import BaseCommand

from DataETL.ETL.DataCleaner import AwMainDataCleaner
from artifacts.models import MaterialTag
import spacy
import json
# Load the language model
nlp = spacy.load("en_core_web_sm")



class Command(BaseCommand):
    help = "Clears caches"

    def handle(self, **options):
        data = []
        service = AwMainDataCleaner()
        targets = service.model_class.objects.all()
        # cluster_materials(materials)
        for target in targets:
            output = {
                'old.pk': target.pk,
                'old.item_number': target.aw_item_number
            }

            material = target.material
            if not material or str(material).strip() == '':
                output['materials'] = []
            else:
                material = service.normalize_material(material)
                doc = nlp(material)
                filtered_tokens = [token.text for token in doc if not token.is_stop]
                output['materials'] = filtered_tokens
                print(f"got {filtered_tokens}")
            data.append(output)
        with open('matiral.json', 'w+' ) as f:
            json.dump(data, f)