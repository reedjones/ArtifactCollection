__author__ = "reed@reedjones.me"

from admin_core.ETL.DataCleaner import AwMainDataCleaner
from legacy_app.models import AwMain


def get_note_fields():
    service = AwMainDataCleaner()
    fields = [str(i).replace("legacy_app.AwMain.", "") for i in service.field_names]
    fields = [i for i in fields if 'note' in i]
    return fields


def has_str(val: str):
    """
    The string is there
    """
    return val is not None and val.strip() != ""


def check_contained_in_other(obj: AwMain, attr_check, attr_alt_source):
    val = getattr(obj, attr_check)
    if has_str(val):
        return  # it's there so we don't need to check
    source = getattr(obj, attr_alt_source)
    if has_str(source):
        return True


def extract_from_other(obj: AwMain, attr, source, extraction_func):
    if check_contained_in_other(obj, attr, source):
        value = extraction_func(obj)
        setattr(obj, attr, value)
        obj.save()
        print(f"Set {attr} to {value}")


def search_missing(awmain: AwMain):
    pass


def clean_note(note):
    note = normalize(note)
    return note


def normalize(val):
    if isinstance(val, str):
        return val.lower()
    elif isinstance(val, list) and isinstance(val[0], str):
        return [i.lower() for i in val]
    return val
