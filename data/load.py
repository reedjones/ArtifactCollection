__author__ = "reed@reedjones.me"
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ArtifactCollection.settings")
import django
django.setup()
import json



from artifacts.models import (
    Artifact, Category, Attribute, Photo,
    ArtifactOwnership, COA, ProvenanceEvent, Period, Person, Collection, County, Region, State, Geography, MaterialTag
)


modeltargets = [Artifact, Category,
           Attribute, Photo,
           ProvenanceEvent, Period,
           Person,Collection, County, Region, Geography, COA,ArtifactOwnership
           ]



def load_or_create(item):
    a, _ = Artifact.objects.get_or_create(
        aw_item_number=item['old.item_number'],

    )
    if _:
        print(f"created {a}")
    else:
        print(f"loaded {a}")
    return a

def final_out():
    for t in modeltargets:
        q = t.objects.count()
        print(f"Total of {q} {t} objects")



def get_files():
    return [i for i in os.listdir('.') if '.json' in i]


def load_json(what):
    with open(what, 'r') as f:
        data = json.load(f)
    return data

def load_cats(data):
    target_value = 'parsed'
    for item in data:
        parsed = item.get(target_value, "")
        print(parsed)
        if not parsed or parsed == '' or parsed == 'None':
            print(item)
        else:
            category = parsed['category']
            cat = Category(
                name=category
            )
            cat.save()
            at = parsed['attr']
            att = Attribute(name=at)
            att.save()
            subcategory = parsed['sub']
            scat = Category(
                parent=cat,
                name=subcategory,
                attribute=att
            )
            scat.save()

            a, _ = Artifact.objects.get_or_create(
                aw_item_number=item['old.item_number'],
                category=scat
            )


def load_county_state(data):
    for item in data:
        if item.get('state', None):

            s = State.objects.filter(short=item.get('state')).first()
            if s:
                g = Geography(state=s)
                g.save()
                if item.get('county', None):
                    c = County(name=item['county'], state=s)
                    c.save()
                    g.county = c
                    g.save()
                    a, _ = Artifact.objects.get_or_create(
                        aw_item_number=item['old.item_number'],

                    )
                    if _:
                        print(f"created {a}")
                    else:
                        print(f"loaded {a}")
                    a.geography = g
                    a.save()

def load_owners(data):
    for item in data:
        target = load_or_create(item)
        if item.get('previous_collections', None):
            for co in item['previous_collections']:
                cname = f"{co} collection"
                p, _ = Person.objects.get_or_create(name=co)

                c, _ = Collection.objects.get_or_create(
                    name=cname, owner=p)
                event = ProvenanceEvent.trigger(
                    actor=c,
                    event_type="owned",
                    artifact=target
                )
                event.save()
                print(event)
                coa = COA(artifact=target)
                coa.save()
                o = ArtifactOwnership(artifact=target,
                                      owner=p,
                                      certification=coa,
                                      collection=c)
                o.save()


def load_photos(data):
    for item in data:
        target = load_or_create(item)
        for k, v in item.items():
            if 'photo' in k and v is not None:
                fname = v.strip()
                if fname:
                    photo = Photo(photo_type=Photo.artifact,
                                  artifact=target,
                                  filename=fname, title=k)
                    photo.save()


def load_regions(data):
    for item in data:
        target = load_or_create(item)
        r = item.get('region', None)
        if r:
            for i in r:
                if i is not None and str(i).strip() != '':
                    region = Region(name=i)
                    region.save()
                    if target.geography:
                        if target.geography.state:
                            region.state = target.geography.state
                        target.geography.region = region
                    else:
                        g = Geography(region=region)
                        g.save()
                        target.geography = g
                    target.save()

def load_materials(data):
    for item in data:
        target = load_or_create(item)
        if item['materials']:
            for matt in item['materials']:
                if matt is not None and matt.strip() != '' and len(matt) > 2:
                    pass


def load_items():
    maps = {
        "cat": "categories.json", #
        "sta": "county_state.json", #
        "last": "dump.json",
        "finder": "finder_owners.json", #
        "mat": "matiral.json",
        "notes": "notes.json",
        "photos": "photos.json", #
        "regions": "regions.json", #
        "states": "states.json", #
    }

    for file in get_files():
        print(f"loading: {file}")
        data = load_json(file)
        if file == maps['regions']:
            for item in data:
                target = load_or_create(item)
                if item.get('materials', None):
                    for matt in item['materials']:
                        if matt is not None and matt.strip() != '' and len(matt) > 2:
                            m, _ = MaterialTag.objects.get_or_create(name=matt)
                            target.materials.add(m)
                            target.save()



if __name__ == '__main__':

    load_items()
    final_out()
