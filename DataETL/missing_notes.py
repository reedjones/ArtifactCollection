__author__ = "reed@reedjones.me"

from django.core.management.base import BaseCommand

from DataETL.ETL.DataCleaner import AwMainDataCleaner
from aw_data.nlp import get_note_fields
import re
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")
import re


def extract_entities(text):
    # Preprocess text
    text = text.lower().replace('\n', ' ').strip()

    # Define regex patterns
    finder_pattern = re.compile(
        r'found\s+by\s+([a-zA-Z\s]+)\s+in\s+([a-zA-Z\s]+)\s+on\s+(\d{1,2}\s+[a-zA-Z]+\s+\d{2,4})')
    purchaser_pattern = re.compile(r'purchased\s+by\s+([a-zA-Z\s]+)\s+on\s+(\d{1,2}\s+[a-zA-Z]+\s+\d{2,4})')
    # Add more patterns for other variations

    # Apply regex patterns
    finder_match = finder_pattern.search(text)
    purchaser_match = purchaser_pattern.search(text)

    # Apply spaCy NER
    doc = nlp(text)

    # Extract entities from spaCy NER
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    return {
        'finder': finder_match.group(1).strip() if finder_match else None,
        'location': finder_match.group(2).strip() if finder_match else None,
        'finder_date': finder_match.group(3).strip() if finder_match else None,
        'purchaser': purchaser_match.group(1).strip() if purchaser_match else None,
        'purchase_date': purchaser_match.group(2).strip() if purchaser_match else None,
        'spaCy_entities': entities
    }


# Example usage
# text = "Found by John Doe in New York on 15 November 2023. Purchased by Alice on 20 December 2023."
# result = extract_entities(text)
#
# print(result)

def coa():
    text = "date 28 april _ 20 13| , signed william m. sherman , no . 0132 ,"

    # Define the regular expression pattern
    pattern = r'\bdate\s+(\d{1,2}\s+[a-zA-Z]+\s+\d{2,4})\s*\|\s*,\s*signed\s+([a-zA-Z\s.]+)\s*,\s*no\s*\.\s*(\d+)\s*'

    # Apply the pattern to the text
    match = re.search(pattern, text)

    # Extract the groups if a match is found
    if match:
        date = match.group(1)
        name = match.group(2)
        certificate_number = match.group(3)

        print(f"Date: {date}")
        print(f"Name: {name}")
        print(f"Certificate Number: {certificate_number}")
    else:
        print("No match found.")

ftargets = [
    'finder',
    'age',
    'previous_collections',
    'condition',
    'aw_type',
    'aw_subtype',
    'site_name',
    'date_found',
    'aw_period',
    # 'aw_grade'
]


def prep_val_name(val: str):
    return val.replace('aw_', "")


alts = {
    'finder': ['found', 'find', 'location', 'saw', 'see'],
    'aw_period': ['time', 'historic', 'age', 'BC', 'period'],
    # 'aw_grade': ['quality', 'score', 'rating', 'grade'],
    'date_found': ['date', 'date found', 'datum', 'day', 'month', 'year'],
    'site_name': ['site', 'spot', 'dig', 'excavation'],
    'previous_collections': ['previous', 'collection', 'former', 'before'],
    'age': ['old', 'date', 'origin', 'alive', 'years'],
    'condition': ['status', 'state', 'wear', 'damage', 'prestine', 'quality', 'structure', 'perfect', 'material'],
    'aw_type': ['type', 'sort', 'kind', 'category', 'class'],
    'aw_subtype': ['subtype', 'category', 'kind', 'sort', 'class'],
}

import re

def make_super_note(obj):
    fields = get_note_fields()
    note = "|"
    for field in fields:
        value = getattr(obj, field)
        if not value:
            value = ""
        note += value + " | "

    return note

r1 = ".|START-"
r2 = "::END-"

def print_sentence_around_match(text, pattern, context_length=20):
    matches = []
    for match in re.finditer(pattern, text):
        sentence_start = max(0, text.rfind('.', 0, match.start()) + 1)
        sentence_end = min(len(text), text.find('.', match.end()))

        start_pos = max(0, sentence_start - context_length)
        end_pos = min(len(text), sentence_end + context_length)

        matched_text = text[start_pos:end_pos].replace(r1, "").replace(r2, "")
        print(f"Match: {match.group()} Context: {matched_text}")
        matches.append(match)
    return matches

import pprint


def check_field(obj, field):
    v = getattr(obj, field)
    if v is not None and not str(v).strip() == '':
        return
    others = alts[field]
    super_note = make_super_note(obj)
    super_note = super_note.lower()
    for ii in ['found', 'find', 'sale', 'purchase', 'purchased', 'located', 'collection']:
        matches = print_sentence_around_match(super_note, ii)
        for match in matches:
            print(f"{obj} has no {field} but notes contain {match.group()}")

    # t = extract_entities(super_note)
    # t2 = {k: v for k, v in t.items() if v is not None}
    # if t2:
    #     pprint.pprint(t2)
    # for other in others:
    #     matches = print_sentence_around_match(super_note, other)
    #     if matches:
    #         print(f"Checking for {field}, found: ")
    #         for match in matches:
    #             print(f"- \t {super_note[match.start():match.end()]}")

        # matches = re.finditer(other, super_note)
        # count = 0
        # for match in matches:
        #     count += 1
        #     print(f"found: {other} in note")
        #     print("match", count, match.group(), "start index", match.start(), "End index", match.end())
        #     start_content = 0
        #     end_content = len(super_note)
        #     s = match.start()
        #     e = match.end()
        #     if not end_content - 100 > e:
        #         ee = e
        #     else:
        #         ee = e + 100
        #     if not s > 100:
        #         ss = s
        #     else:
        #         ss = s - 100
        #     print(f"Snippit: ... '{super_note[ss:ee]}'")




from django.db.models import Q

class Command(BaseCommand):
    help = "Clears caches"

    def handle(self, **options):
        service = AwMainDataCleaner()
        for field in ['finder', 'previous_collections']:
            q = {
                f"{field}__isnull": True,
                f'{field}__exact': ' ',
                f'{field}': '',

            }
            q_object = Q()

            for key, value in q.items():
                q_object |= Q(**{key: value})
            targets = service.model_class.objects.filter(q_object)
            print(f"Got {targets.count()} items with no {field}")
            for target in targets:
                check_field(target, field)

