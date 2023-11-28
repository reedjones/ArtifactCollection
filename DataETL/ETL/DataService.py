__author__ = "reed@reedjones.me"
"""
# Copyright 2023 by Reed Jones
# All rights reserved.
# This file is part of the DjangoChartMaker library,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
"""

import enum
import logging
from abc import ABC
from typing import Type, List, Union

from django import forms
from django.db.models import Sum, Max, Min, F, IntegerField, Avg, TextChoices
from django.db.models.functions import Cast

from .DataCleaner import AwMainDataCleaner, AwImageDataCleaner, DataCleaner
from .charts import ChartChoices, objects_to_df, Chart, PALETTE

logger = logging.getLogger("django")
AggregationTypes = enum.Enum(
    "AggregationTypes", {"Avg": Avg, "Sum": Sum, "Min": Min, "Max": Max}
)


def aggregation_type_from_str(s):
    if hasattr(AggregationTypes, s):
        return getattr(AggregationTypes, s).value


def generate_enum(list_or_dict: Union[List, dict], choices=True, name="Choices"):
    cls = enum.Enum
    if choices:
        cls = TextChoices
    return cls(name, list_or_dict)


class DataService(ABC):
    """
    Generic class for generating forms from django Model class instances that are used for database queries and aggregations
    the class get's unique values for a given field and can generate
        - form select options,
        - autocomplete value lists,
        - django query [dict] that can be sent to a ORM function
        - and QuerySets - from executing queries that it generates
    it contains methods to select the appropriate form input type a given field and return the forms.Field type
    """

    cleaner_class: Type[DataCleaner]
    fields: List[str] = None
    aggregates: List[str] = None
    _populated: bool = False
    choices_getters: List[tuple] = None
    Filters: enum.Enum = None
    Measures: enum.Enum = None
    Aggregations: enum.Enum = None

    def __init__(self, *args, fields=None, populate=True, **kwargs):
        self.cleaner = self.cleaner_class()
        self.model_class = self.cleaner.model_class
        if fields:
            self.fields = fields
        if not self.fields:
            self.fields = self.cleaner.field_names
        if not self.aggregates:
            self.aggregates = []
        if populate:
            self.set_unique_values()
        self.choices_getters = [
            ("filter", self.fields),
            ("measure", self.aggregates),
            ("aggregation", ["Min", "Max", "Sum", "Count"]),
        ]

        for item in self.choices_getters:
            setattr(
                self,
                f"{item[0].capitalize()}s",
                generate_enum(item[1], name=f"{item[0].capitalize()}s", choices=False),
            )
            setattr(
                self,
                f"{item[0]}_text_choices",
                generate_enum(item[1], name=f"{item[0].capitalize()}Choices"),
            )

    def get_chart_form(self, *args, **kwargs):
        filter_choices = getattr(self, "filter_text_choices")
        measure_choices = getattr(self, "measure_text_choices")
        aggregation_choices = getattr(self, "aggregation_text_choices")

        class ChartForm(forms.Form):
            title = forms.CharField(
                max_length=200, widget=forms.TextInput(), initial="My Chart"
            )
            filter_by = forms.ChoiceField(choices=filter_choices.choices)
            measure = forms.ChoiceField(choices=measure_choices.choices)
            aggregation = forms.ChoiceField(
                choices=aggregation_choices.choices, required=True
            )
            chart_type = forms.ChoiceField(choices=ChartChoices.choices)

            limit = forms.IntegerField(
                required=True,
                min_value=1,
                max_value=100,
                help_text="Limit number of items (too many makes for a bad chart)",
                widget=forms.NumberInput(),
                initial=5,
            )

        return ChartForm(*args, **kwargs)

    def get_chart_data(self, chart_form: forms.Form):
        if not chart_form.is_valid():
            return chart_form.errors
        data = chart_form.cleaned_data
        return self.calculation(data["filter_by"], data["measure"], data["aggregation"])

    def get_chart_description(self, chart_form: forms.Form):
        data = chart_form.cleaned_data
        return f"""<strong>{self.model_class.__name__}</strong> models, 
        filtered by their <em>{data['filter_by']}</em> attribute, 
        with the <em>{data['aggregation']}</em> 
        of the measure <em>{data['measure']}</em>. <br> <small><strong>Chart type:</strong> {data['chart_type']} </small>"""

    def make_chart(self, chart_form: forms.Form, title=None):
        if not title:
            title = f"{self.__class__} Generated Chart"
        data = self.get_chart_data(chart_form)
        top = data[: chart_form.cleaned_data["limit"]]
        int_cols = f"{chart_form.cleaned_data['measure']}__{chart_form.cleaned_data['aggregation'].lower()}"
        chart_id = f"{chart_form.cleaned_data['chart_type']}_chart_1"
        df = objects_to_df(
            top,
            fields=data[0].keys(),
            is_values=True,
            int_cols=[int_cols],
        )
        chart_obj = Chart(
            chart_form.cleaned_data["chart_type"], chart_id=chart_id, palette=PALETTE
        )
        chart_obj.from_df(
            df, values=int_cols, labels=[chart_form.cleaned_data["filter_by"]]
        )
        return chart_obj.get_presentation(title=chart_form.cleaned_data["title"])

    def set_unique_values(self):
        for field_name in self.fields:
            setattr(
                self,
                self.get_set_name(field_name),
                self.cleaner.get_unique_for_field(field_name=field_name),
            )
        self._populated = True

    def get_unique_values(self, field):
        if not self._populated:
            self.set_unique_values()
        return getattr(self, self.get_set_name(field))

    def get_from_count(self, field, value):
        q = {field: value}
        return self.model_class.objects.filter(**q).count()

    def print_describe(self):
        for field in self.fields:
            c = self.field_distinct_counts(field)
            logger.debug(f"There are {c} unique values for the field {field}")
            if 50 > c > 1:
                counts = self.get_counts(field)
                for i in counts:
                    clean_value = self.cleaner.clean_weird(
                        i["value"],
                    )
                    if len(clean_value) > 1:
                        self.set_unique(field, clean_value)
                        for unique_value in clean_value:
                            q = {f"{field}__icontains": unique_value}
                            count = self.model_class.objects.filter(**q).count()
                            logger.debug(f"\t value: {unique_value} count: {count}")

                    else:
                        logger.debug(f"\t value: {clean_value} count: {i['count']}")
            logger.debug(f"There are {c} unique values for the field {field}")


    def sum_over(self, field, agg, min_max=False):
        uniques = getattr(self, self.get_set_name(field))
        results = []
        for unique_value in uniques:
            x = {field: unique_value}
            q = {f"{field}__icontains": unique_value}
            if min_max:
                x.update(
                    self.model_class.objects.filter(**q).aggregate(
                        Sum(agg), Min(agg), Max(agg)
                    )
                )
            else:
                x.update(self.model_class.objects.filter(**q).aggregate(Sum(agg)))
            results.append(x)
        return results

    def what_most(self, what, most_of, value):
        """
        -> [what, who, when, where] found the most arrowheads of [class, time-period, material]

        etc... what matirial is most often this time perod
        # what material aw_type Clovis
        what=material, most_of=aw_type, value='Clovis'

        here we are asking what material is most often associated with aw_type clovis
        """
        field = what
        uniques = getattr(self, self.get_set_name(field))
        results = []
        for unique_value in uniques:
            x = {field: unique_value, "agg": most_of, "agg_val": value}
            q = {f"{field}__icontains": unique_value}
            q2 = {f"{most_of}__icontains": value}
            n = self.model_class.objects.filter(**q).filter(**q2).count()
            x.update({f"{most_of}_count": n})
            if x[f"{most_of}_count"]:
                results.append(x)
        return sorted(results, key=lambda d: d[f"{most_of}_count"], reverse=True)

    def what_highest(self, what, value):
        """
        -> what [time period, material, class]
        has the highest [average sale value, appraisal, etc..]
        :param what:
        :param value:
        :return:
        """
        field = what
        result_key = value + "__sum"
        uniques = getattr(self, self.get_set_name(field))
        results = []
        for unique_value in uniques:
            x = {field: unique_value}
            q = {f"{field}__icontains": unique_value}
            x["count"] = self.get_from_count(field, unique_value)
            x.update(self.model_class.objects.filter(**q).aggregate(Sum(value)))
            if not x[result_key]:
                pass
            else:
                # logger.debug(x)
                results.append(x)
        return sorted(results, key=lambda d: d[result_key], reverse=True)

    def calculation(self, what: str, value: str, aggregation: str):
        """
        what [filter option] has the [aggregation option] of [measure option]
        :param what: str name of a `Django.models.Field` type defined on the model [filter option]
        :param value: str name of a `Django.models.Field` type defined on the model [measure option]
        :param aggregation: str name of a `Django.models.Field` type defined on the model [aggregation option]
        :return: a QuerySet
        """
        field = what
        uniques = getattr(self, self.get_set_name(field))
        results = []
        for unique_value in uniques:
            x = {field: unique_value}
            q = {f"{field}__icontains": unique_value}
            x["count"] = self.get_from_count(field, unique_value)
            result_key = value + f"__{aggregation.lower()}"
            aggregation_func = aggregation_type_from_str(aggregation)
            x.update(
                self.model_class.objects.filter(**q).aggregate(aggregation_func(value))
            )
            if not x[result_key]:
                pass
            else:
                # logger.debug(x)
                results.append(x)
        return sorted(results, key=lambda d: d[result_key], reverse=True)

    @staticmethod
    def sl(top=True, bottom=False, l=None, n: int = None):
        if top:
            return l[:n]
        elif bottom:
            return l[n * -1 :]

    @staticmethod
    def get_set_name(val):
        return val + "_set"

    @staticmethod
    def get_count_name(val):
        return val + "_count"

    def set_count(self, field, num):
        setattr(self, self.get_count_name(field), num)

    def set_unique(self, field, value):
        current = getattr(self, self.get_set_name(field))
        x = getattr(self, self.get_count_name(field))
        if isinstance(value, list):
            setattr(self, self.get_count_name(field), x + len(value))
            current += value
        else:
            setattr(self, self.get_count_name(field), x + 1)
            current.append(value)
        setattr(self, self.get_set_name(field), list(set(current)))

    def field_distinct_counts(self, fname):
        unique_values = getattr(self, self.get_set_name(fname))
        count = len(unique_values)
        self.set_count(fname, count)
        return count

    def setup(self):
        for field in self.fields:
            c = self.field_distinct_counts(field)
            setattr(self, self.get_count_name(field), c)

    def get_counts(self, field):
        unique_values_set = getattr(self, self.get_set_name(field))
        items = []
        for unique_value in unique_values_set:
            q = {field: unique_value}
            count = self.model_class.objects.filter(**q).count()
            items.append({"value": unique_value, "field": field, "count": int(count)})
        return items

    def get_clean_values(self, field_name):
        dirty_values = self.get_unique_values(field_name)
        return [self.cleaner.clean_weird(v) for v in dirty_values]


class AwMainService(DataService):
    """
    AwMain.objects.filter(**q)
    .annotate(value_as_int=Cast('value', output_field=IntegerField()))
    .aggregate(Sum('value_as_int'))
    """

    cleaner_class = AwMainDataCleaner
    fields = [
        "region",
        "material",
        "aw_type",
        "aw_subtype",
        "county",
        "site_name",
        "finder",
        "previous_collections",
        "aw_period",
    ]
    aggregates = ["value", "cash_value", "age"]

    def get_clean_regions(self):
        return self.get_clean_values("region")


class AwImagesService(DataService):
    cleaner_class = AwImageDataCleaner
    fields = ["image_author", "image_refno", "image_type", "image_cat_page_no"]
    aggregates = [
        "aw_main_items__value",
        "aw_main_items__cash_value",
        "aw_main_items__age",
    ]


def demo():
    a = AwMainService()
    for field in a.fields:
        c = a.field_distinct_counts(field)
    # top = them[:3]
    # bottom = them[-3:]

    material_with_value = a.what_highest("material", "cash_value")
    region_with_value = a.what_highest("region", "cash_value")
    region_with_price = a.what_highest("region", "purchase_price")
    region_with_old = a.what_highest("region", "age")
    type_with_value = a.what_highest("aw_type", "cash_value")
    type_with_price = a.what_highest("aw_type", "purchase_price")

    logger.debug(material_with_value)
    logger.debug(region_with_price)
    logger.debug(region_with_old)
    state_with_clovis = a.what_most(
        what=a.Filters.aw_state.name, most_of=a.Filters.aw_type.name, value="Clovis"
    )
    logger.debug(region_with_value)
    logger.debug(type_with_price)
    logger.debug(state_with_clovis)

    logger.debug(type_with_value)
    # aw types, with the most common state, and how many are in the state
    logger.debug("types with state")
    atypes_counts = a.get_counts("aw_type")
    astates = a.get_counts("aw_state")
    for ttype in astates:
        most_state = a.what_most(
            what=a.Filters.aw_type.name,
            most_of=a.Filters.aw_state.name,
            value=ttype["value"],
        )[0]
        ttype["aw_type"] = most_state
        ttype["aw_type_total"] = a.get_from_count(
            "aw_type", value=most_state["aw_type"]
        )

    logger.debug("done")
    # items there price, value, and profit
    most_profitable = (
        a.model_class.objects.filter(purchase_price__isnull=False)
        .exclude(purchase_price="0.00")
        .annotate(price_int=(Cast("purchase_price", IntegerField())))
        .annotate(profit=F("cash_value") - F("price_int"))
    )
    most_profitable_info = most_profitable.aggregate(
        Avg("profit"), Max("profit"), Min("profit")
    )

    logger.debug(most_profitable)
    logger.debug(most_profitable_info)
    # AwMain.objects.filter(purchase_price__isnull=False).annotate(price_int=(Cast('purchase_price', IntegerField())))\.annotate(profit=F('cash_value') - F('price_int'))

    logger.debug("done")
