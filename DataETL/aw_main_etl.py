__author__ = "reed@reedjones.me"

from django.core.management.base import BaseCommand

from DataETL.ETL.DataCleaner import AwMainDataCleaner
from .loader import load_value, AwMainLoader, CategoryLoader
from aw_data.models import State, MaterialTag, ArtifactPhoto, Collection, COA, County, Person, Trade
from aw_data.models import ArtifactOwnership as Ownership
from legacy_app.models import AwMain

service = AwMainDataCleaner()


import re


def parse_entries(file_path):
    entries = []

    with open(file_path, 'r') as file:
        current_entry = {}
        for line in file:
            line = line.strip()

            if not line:
                continue  # Skip empty lines

            # Check if the line starts with a number and a period
            if re.match(r'^\d+\.', line):
                # If we have a current entry, add it to the list
                if current_entry:
                    entries.append(current_entry)
                # Start a new entry
                current_entry = {'Item': line.split('.', 1)[1].strip()}
            else:
                # Split the line into key and value
                key, value = map(str.strip, line.split(':', 1))
                current_entry[key] = value

    # Add the last entry if any
    if current_entry:
        entries.append(current_entry)

    return entries

# # Example usage
# file_path = 'your_file.txt'
# parsed_entries = parse_entries(file_path)
#
# for entry in parsed_entries:
#     print(entry)

def ok(v):
    return v is not None and str(v).strip() != ''

def is_done_region(target):
    return bool(target.region and target.state and target.area)


def transform_previous_collections(target, loader):
    pass

def transform_finder(target : AwMain, loader):
    pass


from dateutil import parser

def transform_ownership(target : AwMain, loader):
    harper = Collection.get_default()
    o = Ownership.default_for_artifact(loader.new_obj)
    print(o.in_collection)
    o.description = "Harper Collection "
    if target.purchase_date:
        o.description += f"purchased on {target.purchase_date}"
    # if target.purchase_notes is not None:
    #     o.description += "\n" + target.purchase_notes
    parsed = parser.parse("2011-09-01")
    o.date_start = parsed
    o.save()
    pc = target.previous_collections
    others = service.clean_weird(pc)
    if others:
        for item in others:
            c, _ = Collection.objects.get_or_create(name=item)
            # o2, _ = Ownership.objects.get_or_create(collector=c, artifact=loader.new_obj)
            if _:
                print(f"Created {c}")
            t, _ = Trade.objects.get_or_create(to_party=harper, from_party=c, ownership=o)

            # t, _ = o.previous_collections.add(t)
            if _:
                print(f"Created {t}")
    if ok(target.finder):
        finders = service.clean_weird(target.finder)
        for person in finders:
            p,_ = Person.objects.get_or_create(name=person)
            if _:
                print(f"Created {p}")
            o.found_by = p
    if ok(target.purchase_date):
        parsed = parser.parse("2011-09-01")
        o.date_start = parsed
        o.save()

    # loader.new_obj.update_prov_document()

def transform_categories(target : AwMain, loader):
    c = CategoryLoader(target)
    if ok(target.aw_type):
        print(f"Running on {target}")
        c.get_cats_check()
    c.run()







def transform_photos(target, loader):
    fields = [f"photo{i}" for i in range(1,10)]
    for field in fields:
        at = getattr(target, field)
        if at is not None and str(at).strip() != '':
            pic, _ = ArtifactPhoto.objects.get_or_create(title=field, artifact=loader.new_obj, src=at)
            if _:
                print(f"Created {pic}")


def transform_region(target, loader):
    output = {
        'target.pk':target.pk,
        'target.item_number':target.item_number
    }
    artifact = loader.target_obj
    if is_done_region(artifact):
        return
    region = target.region # old region
    old_state = None
    old_region = None
    old_county = None
    if target.aw_state:
        try:
            s, c = State.objects.get_or_create(short=target.aw_state)
        except Exception as e:
            print(e)
            f = input()
            exit()
        if c:
            print(f"Created {s}")
        if s:
            loader.sets_attr('state', s)
            old_state = s
    if target.county is not None and target.county.strip() != '':
        c, created = County.objects.get_or_create(name=target.county)
        if created:
            print(f"Created {c}")
        if c:
            old_county = c
            if old_state and not c.state:
                c.state = old_state
                c.save()
            artifact.county = c
            artifact.save()
    if region:
        print(f"Testing {target}")
        print(f"old {region}")
        cool = service.clean_region_new(region)
        print(f"Now is {cool}")
        for item in cool:
            done = is_done_region(artifact)
            if done:
                return
            # loaded = test_load_value(item, target)
            loaded = load_value(item, target)
            print(f"Classified {item} as {loaded}")

            if loaded['region'] and not artifact.region:
                artifact.region = loaded['region']
                artifact.save()
            if loaded['state'] and not artifact.state:
                artifact.state = loaded['state']
                artifact.save()
                if old_county and not artifact.county:
                    artifact.county = old_county
            if loaded['area'] and not artifact.area:
                artifact.area = loaded['area']
                if not loaded['area'].state:
                    if old_state:
                        a = loaded['area']
                        a.state = old_state
                        a.save()
                artifact.save()
    noregion = not artifact.region
    nostate = not artifact.state
    nocounty = not artifact.county
    print(f"Region: {not noregion}\n State: {not nostate} \n County: {not nocounty}\n Area {not artifact.area is None}")
    artifact.save()


def transform_materials(target: AwMain, loader: AwMainLoader):
    material = target.material
    if not material or str(material).strip() == '':
        return
    material = service.normalize_material(material)
    for i in ['and', 'with', 'but', 'the', 'a', 'in', 'through', 'around', 'that', 'where']:
        material = material.replace(i, "")
    words = material.split(" ")
    words = [w.strip() for w in words if w]
    for word in words:
        tag, created = MaterialTag.objects.get_or_create(value=word)
        loader.new_obj.materials.add(tag)
    loader.new_obj.save()


def make_super_note(loader):
    return loader.make_super_note()


def make_notes(loader):
    loader.add_notes()



class Command(BaseCommand):
    help = "Clears caches"

    def add_arguments(self, parser):

        parser.add_argument(
            "--regions",
            action="store_true",
            help="Extract, Transform, and Load: region, state, and areas",
        )
        parser.add_argument(
            "--material_tags",
            action="store_true",
            help="Extract, Transform, and Load: materials basic version (tags)",
        )
        parser.add_argument(
            "--notes",
            action="store_true",
            help="Extract, Transform, and Load: notes",
        )
        parser.add_argument(
            "--super_notes",
            action="store_true",
            help="Extract, Transform, and Load: notes combines all notes into 1 super note",
        )
        parser.add_argument(
            "--photos",
            action="store_true",
            help="Extract, Transform, and Load: photos",
        )
        parser.add_argument(
            "--ownership",
            action="store_true",
            help="Extract, Transform, and Load: ownership data",
        )
        parser.add_argument(
            "--categories",
            action="store_true",
            help="Extract, Transform, and Load: category data",
        )

    def handle(self, **options):
        targets = service.model_class.objects.all()
        for target in targets:
            main_loader = AwMainLoader(target)
            if options['regions']:
                transform_region(target, main_loader)
            if options['material_tags']:
                transform_materials(target, main_loader)
            if options['notes']:
                make_notes(main_loader)
            if options['super_notes']:
                make_super_note(main_loader)
            if options['ownership']:
                transform_ownership(target, main_loader)
            if options['categories']:
                print("Running categoires ***********")
                transform_categories(target, main_loader)
            if options['photos']:
                transform_photos(target, main_loader)