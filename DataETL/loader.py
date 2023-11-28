__author__ = "reed@reedjones.me"

import re

from DataETL.ETL.DataCleaner import AwMainDataCleaner
from django.db import models
from .nlp import get_note_fields



class Physical:
    pass



class Physical:
    pass


class TypeCategory:
    pass

class Area:
    pass


class State:
    pass

class Region:
    pass

class MaterialTag:
    pass

class ArtifactModel:
    pass

class Period:
    pass

class Region:
    pass
class Area:
    pass

def ok(v):
    return v is not None and str(v).strip() != ''


def value_exact_replace(value, test_str, subst=""):
    regex = rf"\b{value}\b"
    result = re.sub(regex, subst, test_str, 0)
    return result





class AreaLoader(object):
    """
    loader for Area model
    """
    model = Area

    def __init__(self, value=None):
        self.value = value

    def create(self):
        if self.is_valid:
            area, _ = self.model.objects.get_or_create(name=self.direction, state=State.objects.get(name=self.state))
            return area

    @property
    def direction(self):
        if not self.value:
            return
        return self.__class__.get_direction(self.value)

    @property
    def state(self):
        if not self.value:
            return
        return self.__class__.get_state(self.value)

    @property
    def is_valid(self):
        return self.value and self.__class__.validate(self.value)

    @classmethod
    def get_direction(cls, value):
        states = State.objects.all().values_list('name', flat=True)
        for s in states:
            if s in value:
                value = value_exact_replace(s, value)
                # value = value.replace(s, "")
        value = value.strip()
        return value

    @classmethod
    def get_state(cls, value):
        for d in cls.model.directionalities:
            if d in value:
                value = value_exact_replace(d, value)
                # value = value.replace(d, "")
        value = value.strip()
        return value

    @classmethod
    def validate(cls, value):
        states = State.objects.all().values_list('name', flat=True)
        ds = cls.model.directionalities
        s = cls.get_state(value)
        d = cls.get_direction(value)
        # it should contain a state and a direction and only a state and direction
        return s and d and s in states and d in ds

    @classmethod
    def from_value_with_state(cls, value: str):
        states = State.objects.all()
        for state in states:
            if state.name in value:
                value = value_exact_replace(state.name, value).strip()
                # value = value.replace(state.name, "").strip()
                return cls.model.objects.get_or_create(name=value, state=state)





class RegionLoader(object):
    model = Region

    def __init__(self, value=None):
        self.value = value

    @property
    def is_valid(self):
        return self.value and self.__class__.validate(self.value)

    def create(self):
        if self.is_valid:
            region, _ = self.model.objects.get_or_create(name=self.value)
            return region

    @classmethod
    def validate(cls, value):
        # we remove any state,
        # and remove any direction,
        # if there is something still there -> it is valid
        states = State.objects.all().values_list('name', flat=True)
        d = cls.model.directionalities
        for i in d:
            value = value_exact_replace(i, value)
            # if i in value:
            #     value = value.replace(i, "")
        for s in states:
            value = value_exact_replace(s, value)

            # if s in value:
            #     value = value.replace(s, "")
        value = value.strip()
        print(f"validating if {value} is none")
        return bool(value)




def setup_states_and_areas():
    if not State.objects.exists():
        State.load()
    states = State.objects.all()
    for state in states:
        for d in State.directionalities:
            area = Area(name=d, state=state)
            area.save()


def test_load_value(value: str, target, recur=None):
    state_names = State.objects.all().values_list('name', flat=True)
    if AreaLoader.validate(value):
        return 'area'
    else:
        print(f"{value} not an Area")
    if RegionLoader.validate(value):
        return 'region'
    else:
        print(f"{value} not a Region")
        if not recur:
            print(f"{value} not either, will retry")
            if len(value.split()) == 1 and value in Area.directionalities:
                if target.aw_state:
                    state = State.objects.filter(short=target.aw_state.upper()).first()
                    if state:
                        return test_load_value(f"{value} {state.name}", target, recur=True)
                    else:
                        print(f"State matching {target.aw_state} Not Found")
                else:
                    print(f"Item has no state")
            elif value in state_names:
                return "state"
            elif all([v in Area.directionalities for v in value.split()]):
                return "Dumb region"
        return f"Not Sure"


def load_value(value: str, target, recur=False):
    state_names = State.objects.all().values_list('name', flat=True)
    data = {
        'area': None,
        'region': None,
        'state': None,
        'county': None
    }

    if not target.aw_state:
        for state in state_names:
            if state in value:
                data['state'] = State.objects.filter(name=state).first()
    else:
        s = State.objects.filter(short=target.aw_state).first()
        if s:
            data['state'] = s

    if AreaLoader.validate(value):
        area = AreaLoader(value)
        data['area'] = area.create()
    if RegionLoader.validate(value):
        region = RegionLoader(value)
        data['region'] = region.create()
    else:
        print(f"{value} not a Region")
        if not recur:
            print(f"{value} not either, will retry")
            if len(value.split()) == 1 and value in Area.directionalities:
                if target.aw_state:
                    state = State.objects.filter(short=target.aw_state.upper()).first()
                    if state:
                        return load_value(f"{value} {state.name}", target, recur=True)
                    else:
                        print(f"State matching {target.aw_state} Not Found")
                else:
                    print(f"Item has no state")
            elif value in state_names:
                sss = State.objects.filter(name=value).first()
                if sss:
                    data['state'] = sss
            elif all([v in Area.directionalities for v in value.split()]) and not data['region']:
                cr, _ = Region.objects.get_or_create(name=f"{target.aw_state} {value}")
                data['region'] = cr
        # return "Not Sure"
        if value is not None and not value.strip() == "":
            if data['state'] and not data['region']:
                rr, c = Region.objects.get_or_create(name=f"{data['state']} {value}")
                data['region'] = rr
    return data


class ArtifactNote:
    pass


class AwMain:
    pass


class AwMainLoader(object):
    model = ArtifactModel

    def sets_attr(self, set_what: str, to_what, target=None, dosave=True):
        if not target:
            target = self.new_obj
        setattr(target, set_what, to_what)
        print(f"set {set_what} to {to_what} on {target}")
        if dosave:
            target.save()

    def gets_attr(self, set_what: str, target=None):
        if not target:
            target = self.new_obj
        getattr(target, set_what)

    @property
    def target_obj(self) -> ArtifactModel:
        return self.new_obj

    def __init__(self, obj: AwMain):
        self.obj = obj
        self.service = AwMainDataCleaner()
        self.new_obj = self.start()

    def start(self):
        print(f"Got awmain {self.obj} with {self.obj.pk}")

        newo, created = ArtifactModel.objects.get_or_create(awmain=self.obj.id)
        if created:
            print(f"Created: {newo}")
        else:
            print(f"Loaded: {newo}")

        return newo

    def make_super_note(self):
        import uuid
        note_fields = get_note_fields()
        note = ""
        for field in note_fields:
            value = str(getattr(self.obj, field))
            if value:
                note += value + "\n"

        return note

    def add_notes(self):
        note_fields = get_note_fields()
        for nf in note_fields:
            value = str(getattr(self.obj, nf))
            if value is not None and not value.strip() == '':
                t, _ = ArtifactNote.objects.get_or_create(artifact=self.new_obj, text=value, name=nf)


from itertools import chain


def flatten_chain(matrix):
    return list(chain.from_iterable(matrix))


def parse_category(category):
    category = category.replace("Point", "Projectile Point")
    # Extract and remove content within parentheses
    parentheses_content = re.search(r'\((.*?)\)', category)
    content_to_remove = ""
    if parentheses_content:
        content_to_remove = parentheses_content.group(0)
        category = category.replace(content_to_remove, '').strip()

    words = category.split()
    main_type_match = re.search(r'\((.*?)\)$', category)

    if main_type_match:
        main_type = main_type_match.group(1)
    else:
        main_type = words[-1] if words[-1] != ')' else words[-2]

    words.pop(-1) if main_type == words[-1] else None
    type_str = ' '.join(words)
    individual_types = type_str.split()

    return {
        'main_type': main_type,
        'type': type_str,
        'individual_types': individual_types,
        "removed":content_to_remove,
    }
import functools

@functools.lru_cache
def load(fp):
    with open(fp, 'r') as f:
        lines = f.readlines()
    return lines

def parse_text_file(file_path):
    entries = []
    lines = load(file_path)
    entry = {}
    for line in lines:
        line = line.strip()
        if line.startswith("Category:"):
            entry["category"] = line.split(":")[1].strip()
        elif line.startswith("Sub-Category:"):
            entry["sub_category"] = line.split(":")[1].strip()
        elif line.startswith("Attribute:"):
            entry["attribute"] = line.split(":")[1].strip()
        elif line:
            entry["name"] = line
            entries.append(entry)
            entry = {}

    return entries


@functools.lru_cache
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
            elif ':' in line:
                # Split the line into key and value only if there is a colon
                key, value = map(str.strip, line.split(':', 1))
                current_entry[key] = value

    # Add the last entry if any
    if current_entry:
        entries.append(current_entry)
    return entries







class CategoryLoader(AwMainLoader):
    model = ArtifactModel

    def get_cats_check(self):
        if not ok(self.obj.aw_type):
            print("val not ok")
            return
        entries = parse_entries("cats_new.txt")
        print(len(entries))
        for entry in entries:
            print(f"checking {entry} {self.obj.aw_type}")
            entry['Item'] = entry['Item'].replace(":", "")
            if entry['Item'] == self.obj.aw_type:
                return {
                    'category':entry['- Category'],
                    'sub':entry['- Sub-Category'],
                    'attr':entry['- Attribute']
                }
                # tc1, _ = TypeCategory.objects.get_or_create(name=entry['- Category'])
                # tc2, __ = TypeCategory.objects.get_or_create(name=entry['- Sub-Category'], parent=tc1)
                # tc3, ___ = TypeCategory.objects.get_or_create(name=entry['Item'], parent=tc2)
                # tc4, ____ = TypeCategory.objects.get_or_create(name=entry['- Attribute'], parent=tc3)
                # self.new_obj.physical.category = tc1
                # self.new_obj.physical.subcategory = tc2
                # self.new_obj.physical.attribute = tc4
                # self.new_obj.type_category = tc3
                # self.new_obj.physical.save()
                # self.new_obj.save()
                # print(f"Object: {tc1} {tc2} {tc3} {tc4}\n {_} {__} {___} {____}")
                # return


    def setup_periods(self):
        ps = self.get_period_options()
        for p in ps:
            period, _ = Period.objects.get_or_create(name=p)
            if _:
                print(f"Created {period}")

    def setup_cat(self, item : str):
        result = parse_category(item)
        main_type = result['individual_types'][-1]
        level_2 = result['main_type'] + main_type
        level_3 = result['type']


    def clean_cat(self, item):
        print(self)
        parts_first = item.split("(")
        subtype = None
        if len(parts_first) > 1:
            subtype = parts_first.pop(-1)
            subtype = subtype.replace(")", "").strip()
            subtype, _ = TypeCategory.objects.get_or_create(name=subtype)
        parts_first = parts_first[0]
        parts_first = parts_first.split(" ")
        parts_first = [i.strip() for i in parts_first]
        if parts_first:
            main_type = parts_first.pop(-1)
            mtc, _ = TypeCategory.objects.get_or_create(name=main_type)
            if subtype:
                subtype.parent = mtc
                subtype.save()
            if parts_first:
                next_type = ' '.join(parts_first)
                if _:
                    print(f"Created {mtc}")
                if len(parts_first) > 1:
                    for part in parts_first:
                        tc, _ = TypeCategory.objects.get_or_create(name=part)
                        tc.parent = main_type
                        if _:
                            print(f"Created {tc}")

    def run(self):
        if not self.new_obj.physical:

            physical = Physical()
            physical.save()
            self.new_obj.physical = physical
            self.new_obj.save()
        physical = self.new_obj.physical
        pc = self.resolve_condition()
        if pc:
            physical.condition = pc
        per = self.resolve_period()
        if per:
            physical.period = per


    def resolve_condition(self):
        if self.obj.condition:
            con = self.__class__.clean_condition(self.obj.condition)
            if con:
                return con
        super_note = self.make_super_note()
        super_note = super_note.lower()
        vals = ['excellent', 'damaged']
        for val in vals:
            if val in super_note:
                return Physical.ConditionType(val)


    def get_period_options(self):
        options = self.service.get_unique_for_field('aw_period')
        cleans = [self.service.clean_weird(opt) for opt in options]
        cleans = flatten_chain(cleans)
        cleans = [i for i in cleans if len(i) > 2 and not i.strip() == 'Historic']
        try:
            cleans.pop(cleans.index('MLate Archaic'))
        except ValueError:
            pass
        return list(set([j.strip().lower() for j in cleans]))

    def resolve_period(self):
        opts = self.get_period_options()
        if ok(self.obj.aw_period):
            print(f"Checking period")
            clean = self.obj.aw_period.strip().lower()
            print(f"Checking {clean}")
            for c in opts:
                print(f"checking {c} in {opts}")
                if c and clean and c == clean:
                    print(f"{c} == {clean}")
                    period, _ = Period.objects.get_or_create(name=c)
                    if _:
                        print(f"Created {period}")
                    return period
        else:
            super_note = self.make_super_note()
            super_note = super_note.lower()
            for opt in opts:
                if opt in super_note:
                    period, _ = Period.objects.get_or_create(name=opt)
                    return period
        return None


    @classmethod
    def clean_condition(cls, v):
        v = v.lower()
        try:
            s = Physical.ConditionType(v)
            return s
        except ValueError:
            for tup in Physical.ConditionType.choices:
                for val in tup:
                    if v in val or val in v:
                        return Physical.ConditionType(val)
            if 'good' in v:
                return Physical.ConditionType.good
        return None
