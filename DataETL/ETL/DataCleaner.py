__author__ = "reed@reedjones.me"
"""
# Copyright 2023 by Reed Jones
# All rights reserved.
# This file is part of the DjangoChartMaker library,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
"""

import logging
import re
from abc import ABC
from typing import Type

from django.db import models

from legacy_app.models import AwMain, AwImages

logger = logging.getLogger("django")


class DataCleaner(ABC):
    model_class: Type[models.Model]
    field_names = None

    def __init__(self, *args, **kwargs):
        """
        Initializes the DataCleaner with the model class and retrieves all field names for the model.
        """
        self.field_names = self.model_class._meta.get_fields()

    @classmethod
    def get_unique_values(cls, values_list, field_name):
        """
        Utility method that takes in a list of objects
        and a field name and returns a list of unique values for that field.

        :param values_list:
        :param field_name:
        :return:
        """

        result = set()  # create an empty set to store unique values
        # loop through the list to extract values
        for v in values_list:
            # check if the field exists and is a list
            if v.get(field_name) and isinstance(v[field_name], list):
                # loop through the list and add the values to the result set
                for i in v[field_name]:
                    result.add(i)
            # check if the field is a string
            elif isinstance(v[field_name], str):
                # add the string to the result set
                result.add(v[field_name])

        filtered = [x for x in result if x]
        return list(filtered)  # convert the set to a list and return it

    def get_unique_for_field(self, field_name):
        """
        Retrieves unique values for a given field name from the model class.
        :param field_name: str
        :return: List[str]
        """
        field_name_filter = field_name + "__isnull"
        items = (
            self.model_class.objects.filter(**{field_name_filter: False})
            .values(field_name)
            .distinct()
        )
        return self.get_unique_values(items, field_name)

    @classmethod
    def clean_weird(cls, weird_string):
        if not weird_string or not isinstance(weird_string, str):
            logger.debug(
                f"Warning {weird_string} isn't a {str} its a {type(weird_string)}"
            )
            return weird_string
        return weird_string.strip().replace("~", ",").strip(",").split(",")

def value_exact_replace(value, test_str, subst=""):
    regex = rf"\b{value}\b"
    result = re.sub(regex, subst, test_str, 0)
    return result
class AwImageDataCleaner(DataCleaner):
    model_class = AwImages


class AwMainDataCleaner(DataCleaner):
    # model_class = AwMain

    def get_old(self):
        return AwMain.objects.using('old').all()
    @property
    def model_class(self) -> Type[AwMain]:
        return AwMain

    @classmethod
    def clean_found_site(cls, word):
        r = "[f|F]ound[\w\s]+(?P<name>[A-Z][a-z]*(\s[A-Z][a-z]*))"
        match = re.search(r, word)
        result = match.group("name")
        return result

    def get_regions(self):
        regions = (
            self.model_class.objects.filter(region__isnull=False)
            .values("region")
            .distinct()
        )
        for r in regions:
            r["region"] = self.clean_weird(r["region"])
        return regions

    def get_materials(self):
        materials = (
            self.model_class.objects.filter(material__isnull=False)
            .values("material")
            .distinct()
        )
        for r in materials:
            r["material"] = self.clean_weird(r["material"])
        return materials

    @classmethod
    def clean_regions(cls, regions):
        region_values = []
        for r in regions:
            if r["region"] and isinstance(r["region"], list):
                for i in r["region"]:
                    if i not in region_values:
                        region_values.append(i)
            elif isinstance(r["region"], str):
                if r["region"] not in region_values:
                    region_values.append(r["region"])
        return [i for i in region_values if i]

    @classmethod
    def clean_materials(cls, materials):
        materials_values = []
        for r in materials:
            if r["material"] and isinstance(r["material"], list):
                for i in r["material"]:
                    if i and i not in materials_values:
                        materials_values.append(i)
            elif isinstance(r["material"], str):
                if r["material"] not in materials_values:
                    materials_values.append(r["material"])
        return [i.lower() for i in materials_values if i]

    @classmethod
    def normalize_material(cls, material):
        # Convert to lowercase and remove extra spaces
        normalized_material = material.lower().strip()
        return normalized_material

    @classmethod
    def convert_directional(cls, value):
        # Split the value into words
        value = value.title()
        value = value_exact_replace("South East", value, "Southeast")
        value = value_exact_replace("South West", value, "Southwest")
        value = value_exact_replace("North West", value, "Northwest")
        value = value_exact_replace("North East", value, "Northeast")
        return value
    def clean_region_new(self, region_value):

        # regions = self.get_unique_for_field('region')
        cleaned_regions = [self.clean_weird(region_value)]
        flattened_data = [location for sublist in cleaned_regions for location in sublist]
        cleaned_locations = list(set(location.strip().title() for location in flattened_data))
        cleaned_locations = [i.replace('/', ' ').replace('Tx', 'Texas').replace('La', 'Louisiana') for i in
                             cleaned_locations]
        cleaned_locations = [i.replace('Se', 'Southeast') for i in cleaned_locations]

        cleaned_locations = [i.replace("","") for i in cleaned_locations]
        # cleaned_locations.append("Texas Central North")
        cleaned_locations = [i.replace("South Western Area Of", "Southwest") for i in cleaned_locations]
        cleaned_locations = [self.convert_directional(i) for i in cleaned_locations]

        for idx, i in enumerate(cleaned_locations):
            if i == 'Texas Central N':
                cleaned_locations.pop(idx)
                cleaned_locations.append("North Central Texas")

            elif i == 'East Texas Louisiana':
                cleaned_locations.pop(idx)
                cleaned_locations.append("East Texas")
                cleaned_locations.append("Texas-Louisiana Border")

            elif i == 'South East Texas Louisiana':
                cleaned_locations.pop(idx)
                cleaned_locations.append("Southeast Texas")
                cleaned_locations.append("Texas-Louisiana Border")
            elif i == 'South East Texas':
                cleaned_locations.pop(idx)
                cleaned_locations.append("Southeast Texas")
        return list(set(cleaned_locations))

    def region_with_clean(self):
        v = self.get_unique_for_field('region')
        for old in v:
            cleaned = self.clean_region_new(old)
            yield (old, cleaned)


    def clean_previous_collection(self):
        prevs = self.get_unique_for_field('previous_collections')
        clean = [self.clean_weird(p) for p in prevs]
        for c in clean:
            for idx, other in c:
                if not other:
                    c.pop(idx)
        return clean




