from django.core.management.base import BaseCommand
import json

photos = [f"photo{i}" for i in range(1,10)]

fields = [
    'county',
    'aw_subtype',
    'aw_type',
    'age',
    'aw_item_number',
    'region',
    'county',
    'aw_state',
    'site_name',
    'condition',
    'date_found',
    'previous_collections',
    'material',
    'aw_period',
    'aw_grade',
    'aw_references',
    'ref_transaction',
    'aw_type_category',
    'river_drainage'
]
fields += photos


class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):
        with open("dump.json", 'r') as f:
            data = json.load(f)
        for item in data:
            print(f"current {item['pk']}")
