__author__ = "reed@reedjones.me"

from abc import ABC, abstractmethod
from datetime import date
from typing import Optional, Type
from .serializers import get_serial_for_model
from django.apps import apps
from django.db import models
from django.db.models import Avg, Sum, Model, Count
from django.db.models import IntegerField, CharField
from django.db.models import QuerySet

# from myapp.models import MyModel  # Replace 'myapp' and 'MyModel' with your actual Django app and model names
from artifacts.models import Artifact

import logging
import sys
from autologging import logged, TRACE, traced
logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, format="HIHI%(levelname)s:%(filename)s,%(lineno)d:%(name)s.%(funcName)s:%(message)s")

@logged
class DataService(ABC):
    """
    Generic class for generating forms from Django Model class instances that are used for database queries and aggregations.
    The class gets unique values for a given field and can generate:
        - form select options,
        - autocomplete value lists,
        - Django query [dict] that can be sent to an ORM function,
        - and QuerySets from executing queries that it generates.
    It contains methods to select the appropriate form input type for a given field and return the forms.Field type.


    data_service = DataServiceImplementation()
    choices = data_service.get_field_choices('name')
    # Example Output: [{'value': 'Option1', 'label': 'Option1'}, {'value': 'Option2', 'label': 'Option2'}, ...]

    data_service = DataServiceImplementation()
    chart_data = data_service.generate_chart_data('value', 'name')
    # Example Output: {'labels': ['Option1', 'Option2', ...], 'data': [sum_value1, sum_value2, ...]}

    data_service = DataServiceImplementation()
    autocomplete_data = data_service.autocomplete_data('name')
    # Example Output: [{'value': 'Option1', 'label': 'Option1'}, {'value': 'Option2', 'label': 'Option2'}, ...]

    data_service = DataServiceImplementation()
    model_info = data_service.get_model_info()
    # Example Output: {'model_name': 'MyModel', 'fields': [{'name': 'name', 'type': 'CharField'}, ...]}


    data_service = DataServiceImplementation()
    form_fields = data_service.get_form_fields()
    # Example Output: {'model_name': 'MyModel', 'fields': {'name': 'CharField', 'value': 'IntegerField', ...}}

    data_service = DataServiceImplementation()
    form_data = {'name': 'Option1', 'value__gte': 50}  # Example form data
    filtered_records = data_service.filter_records_by_form(form_data)
    # Example Output: QuerySet of records that match the specified form data conditions

    """

    class Meta:
        model = None  # Users must provide the model

    def get_sorted_and_paginated_data(self, sort_field: str, ascending: bool, page: int, page_size: int) -> QuerySet:
        """
        Sorting and Pagination:

            Method Name: get_sorted_and_paginated_data
            Purpose: Allow clients to retrieve paginated and sorted data based on a specified field.
            Parameters:
            sort_field: Name of the field to sort the data.
            ascending: Boolean indicating whether to sort in ascending or descending order.
            page: Page number for paginated results.
            page_size: Number of records per page.
        :param sort_field:
        :param ascending:
        :param page:
        :param page_size:
        :return:
        """
        queryset = self.Meta.model.objects.all().order_by(sort_field if ascending else f'-{sort_field}')
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        return queryset[start_index:end_index]

    def search_records(self, search_field: str, search_query: str) -> QuerySet:
        """
        Searching Records:

            Method Name: search_records
            Purpose: Allow clients to search records based on a specified field and search query.
            Parameters:
            search_field: Name of the field to search.
            search_query: The search query.
            Implementation:
        :param search_field:
        :param search_query:
        :return:
        """
        return self.Meta.model.objects.filter(**{f'{search_field}__icontains': search_query})

    def aggregate_for_multiple_fields(self, aggregation_fields: list) -> dict:
        """
        ggregating Data for Multiple Fields:

            Method Name: aggregate_for_multiple_fields
            Purpose: Enable clients to perform aggregations on multiple fields simultaneously.
            Parameters:
            aggregation_fields: List of fields for which to perform aggregations.
            Implementation:
        :param aggregation_fields:
        :return:
        """
        result = {}
        for field in aggregation_fields:
            result[field] = self.average_value(field)  # Or other aggregation method
        return result

    def export_data(self, export_format: str, **kwargs) -> str:
        """
        Exporting Data to Different Formats:

            Method Name: export_data
            Purpose: Allow clients to export data in various formats like CSV, JSON, or Excel.
            Parameters:
            export_format: The desired export format (e.g., 'csv', 'json', 'excel').
            Additional format-specific parameters.
            Implementation:
        :param export_format:
        :param kwargs:
        :return:
        """
        # Implementation to export data in the specified format
        if export_format == 'csv':
            return self.export_to_csv(**kwargs)
        elif export_format == 'json':
            return self.export_to_json(**kwargs)
        else:
            raise ValueError(f"Unsupported export format: {export_format}")

    def sum_grouped_by_field(self, value_field: str, group_by_field: str) -> QuerySet:
        """
        Method Name: sum_grouped_by_field
            Purpose: Calculate the sum of values grouped by another field.
            Parameters:
            value_field: Name of the field to sum.
            group_by_field: Name of the field to group by.
        :param value_field:
        :param group_by_field:
        :return:
        """
        return self.Meta.model.objects.values(group_by_field).annotate(sum_value=Sum(value_field))

    def export_to_csv(self, *args, **kwargs):
        raise NotImplemented

    def export_to_json(self, *args, **kwargs):
        raise NotImplemented

    def count_records(self, condition_field: str, condition_value: str) -> int:
        """
        Method Name: count_records
            Purpose: Count the number of records in the database that match a specific condition.
            Parameters:
            condition_field: Name of the field to filter on.
            condition_value: Value to filter for in the specified field.
            Implementation:
        :param condition_field:
        :param condition_value:
        :return:
        """
        return self.Meta.model.objects.filter(**{condition_field: condition_value}).count()

    def filter_by_date_range(self, date_field: str, start_date: date, end_date: date) -> QuerySet:
        """
        Method Name: filter_by_date_range
            Purpose: Retrieve records within a specified date range.
            Parameters:
            date_field: Name of the date field to filter on.
            start_date: Start date of the range.
            end_date: End date of the range.
        :param date_field:
        :param start_date:
        :param end_date:
        :return:
        """
        return self.Meta.model.objects.filter(**{f'{date_field}__range': (start_date, end_date)})

    def average_value(self, numeric_field: str) -> float:
        """
        Get Average Value for a Field:

            Method Name: average_value
            Purpose: Calculate the average value of a numeric field.
            Parameters:
            numeric_field: Name of the numeric field to calculate the average for.
            Implementation:
        :param numeric_field:
        :return:
        """
        return self.Meta.model.objects.aggregate(avg_value=Avg(numeric_field))['avg_value'] or 0.0

    def latest_n_records(self, order_field: str, n: int) -> QuerySet:
        """
        Method Name: latest_n_records
            Purpose: Retrieve the latest N records based on a specified field.
            Parameters:
            order_field: Name of the field to order the records by.
            n: Number of records to retrieve.
            Implementation:
        :param order_field:
        :param n:
        :return:
        """
        return self.Meta.model.objects.all().order_by(f'-{order_field}')[:n]

    def distinct_values(self, distinct_field: str) -> list:
        """
        Distinct Values for a Field:
            Method Name: distinct_values
            Purpose: Get a list of distinct values for a specific field.
            Parameters:
            distinct_field: Name of the field for which to get distinct values.
        :param distinct_field:
        :return:
        """
        return list(self.Meta.model.objects.values_list(distinct_field, flat=True).distinct())

    def get_field_choices(self, field_name: str) -> list:
        """
        Get Field Choices for a Select Input:

            Method Name: get_field_choices
            Purpose: Provide choices for a frontend select input based on the unique values of a field.
            Parameters:
            field_name: Name of the field for which to get choices.
            Implementation:
        :param field_name:
        :return:
        """
        print(f"get field choices called with {field_name}")
        return [{'value': value, 'label': str(value)} for value in self.distinct_values(field_name)]

    @abstractmethod
    def calculation(self, what: str, value: str, aggregation: str) -> QuerySet:
        """
        Generate a QuerySet based on a calculation query.

        Parameters:
        - what (str): Name of a `Django.models.Field` type defined on the model [filter option].
        - value (str): Name of a `Django.models.Field` type defined on the model [measure option].
        - aggregation (str): Name of a `Django.models.Field` type defined on the model [aggregation option].

        Returns:
        QuerySet: Resulting queryset based on the calculation query.
        """

    @abstractmethod
    def what_highest(self, what: str, value: str, other_field: str) -> QuerySet:
        """
        Find the record with the highest value for a specific field related to another field.

        Parameters:
        - what (str): Name of the field to check for the highest value.
        - value (str): Name of the field to consider for the value.
        - other_field (str): Name of the related field.

        Returns:
        QuerySet: Resulting queryset with the record having the highest value for the specified field.
        """

    @abstractmethod
    def what_most(self, what: str, most_of: str, value: str, optional_other_field: Optional[str] = None) -> QuerySet:
        """
        Find the record with the most occurrences of a specific value for a field.

        Parameters:
        - what (str): Name of the field to check for the most occurrences.
        - most_of (str): Name of the value to count occurrences.
        - value (str): Name of the field to consider for the value.
        - optional_other_field (str, optional): Name of an optional related field.

        Returns:
        QuerySet: Resulting queryset with the record having the most occurrences of the specified value.
        """

    @abstractmethod
    def autocomplete_values(self, field_name: str) -> list:
        """
        Get autocomplete values for a specific field.

        Parameters:
        - field_name (str): Name of the field for which autocomplete values are needed.

        Returns:
        list: List of unique values for the specified field.
        """

    @abstractmethod
    def form_select_options(self, field_name: str) -> list:
        """
        Get form select options for a specific field.

        Parameters:
        - field_name (str): Name of the field for which select options are needed.

        Returns:
        list: List of unique values for the specified field.
        """

    @abstractmethod
    def form_field_type(self, field_name: str) -> str:
        """
        Get the appropriate form field type for a specific field.

        Parameters:
        - field_name (str): Name of the field for which the form field type is needed.

        Returns:
        str: Form field type for the specified field.
        """

    @abstractmethod
    def generate_chart_data(self, value_field: str, group_by_field: str = None) -> dict:
        """
        Method Name: generate_chart_data
            Purpose: Create data suitable for rendering charts in the frontend.
            Parameters:
            value_field: Name of the field to visualize.
            group_by_field: Name of the field to group data by (e.g., for bar charts).
            Implementation:
        :param value_field:
        :param group_by_field:
        :return:
        """
        data = self.sum_grouped_by_field(value_field, group_by_field) if group_by_field else \
            [{'group': 'All', 'sum_value': self.average_value(value_field)}]
        return {'labels': [item['group'] for item in data], 'data': [item['sum_value'] for item in data]}

    @abstractmethod
    def autocomplete_data(self, field_name: str) -> list:
        """
        Method Name: autocomplete_data
            Purpose: Provide data for autocompleting input fields.
            Parameters:
            field_name: Name of the field for which to retrieve autocomplete data.
            Implementation:
        :param field_name:
        :return:
        """
        return [{'value': value, 'label': str(value)} for value in self.autocomplete_values(field_name)]

    @abstractmethod
    def get_model_info(self) -> dict:
        """
        Get Model Information for Frontend Display:

            Method Name: get_model_info
            Purpose: Provide information about the model for rendering in the frontend.
            Parameters:
            None
        :return:
        """
        pass

    @abstractmethod
    def model(self) -> Type[Model]:
        pass


@traced
class DataServiceImplementation(DataService):
    # class Meta:
    #     model = Artifact  # Replace with the appropriate model

    class Meta:
        model_name = None
        model = None

    @property
    def model(self) -> Type[Model]:
        return self.Meta.model

    def __init__(self, app_name, model_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.model = apps.get_model(app_name, model_name)
        self._serializer = get_serial_for_model(self.Meta.model)

    def serialize(self, data, many=True, **kwargs):
        if isinstance(data, QuerySet):
            serializer = self._serializer(data, many=many, **kwargs)
            serialized_data = serializer.data
        else:
            serialized_data = data
        return serialized_data

    def generate_chart_data(self, value_field: str, group_by_field: str = None) -> dict:
        """
        Method Name: generate_chart_data
            Purpose: Create data suitable for rendering charts in the frontend.
            Parameters:
            value_field: Name of the field to visualize.
            group_by_field: Name of the field to group data by (e.g., for bar charts).
            Implementation:
        :param value_field:
        :param group_by_field:
        :return:
        """
        data = self.sum_grouped_by_field(value_field, group_by_field) if group_by_field else \
            [{'group': 'All', 'sum_value': self.average_value(value_field)}]
        return {'labels': [item['group'] for item in data], 'data': [item['sum_value'] for item in data]}

    def autocomplete_data(self, field_name: str) -> list:
        """
        Method Name: autocomplete_data
            Purpose: Provide data for autocompleting input fields.
            Parameters:
            field_name: Name of the field for which to retrieve autocomplete data.
            Implementation:
        :param field_name:
        :return:
        """
        return [{'value': value, 'label': str(value)} for value in self.autocomplete_values(field_name)]

    def get_model_info(self) -> dict:
        """
        Get Model Information for Frontend Display:

            Method Name: get_model_info
            Purpose: Provide information about the model for rendering in the frontend.
            Parameters:
            None
        :return:
        """
        fields = [{'name': field.name, 'type': self.form_field_type(field.name)} for field in
                  self.Meta.model._meta.fields]
        return {'model_name': self.Meta.model.__name__, 'fields': fields}

    def get_form_fields(self) -> dict:
        """
        Get Form Fields for Frontend Form Creation:

            Method Name: get_form_fields
            Purpose: Provide information about form fields for frontend form creation.
            Parameters:
            None
            Implementation:
        :return:
        """
        fields = {field.name: self.form_field_type(field.name) for field in self.Meta.model._meta.fields}
        return {'model_name': self.Meta.model.__name__, 'fields': fields}

    def execute_custom_query(self, query: str) -> QuerySet:
        """
        Handling Complex Queries:

            Method Name: execute_custom_query
            Purpose: Allow clients to execute custom queries on the database.
            Parameters:
            query: Custom query to execute.
            Implementation:
        :param query:
        :return:
        """
        # Implementation to execute the custom query
        return self.Meta.model.objects.raw(query)
        # Rest of the class implementation...

    def calculation(self, what: str, value: str, aggregation: str) -> QuerySet:
        """
        Implementation of the calculation method.
        """
        # Your custom implementation based on the provided parameters
        # Example: return MyModel.objects.filter(**{what: value}).annotate(result=Sum(aggregation))
        return self.model.objects.filter(**{what: value}).annotate(result=Sum(aggregation))

    def what_highest(self, what: str, value: str, other_field: str) -> QuerySet:
        """
        Implementation of the what_highest method.
        """
        # Your custom implementation based on the provided parameters
        # Example: return MyModel.objects.filter(**{other_field: value}).order_by('-'+what).first()
        return self.model.objects.filter(**{other_field: value}).order_by('-' + what).first()

    def what_most(self, what: str, most_of: str, value: str, other_field: Optional[str] = None,
                  other_value: Optional[str] = None) -> QuerySet:
        """
        Implementation of the what_most method.
        """
        # Your custom implementation based on the provided parameters
        # Example: filter_args = {what: value}
        # if optional_other_field:
        #     filter_args[optional_other_field] = some_value
        # return MyModel.objects.filter(**filter_args).annotate(count=Count(most_of)).order_by('-count').first()
        filter_args = {what: value}
        if other_field:
            filter_args[other_field] = other_value
        return self.model.objects.filter(**filter_args).annotate(count=Count(most_of)).order_by('-count').first()

    def autocomplete_values(self, field_name: str) -> list:
        """
        Implementation of the autocomplete_values method.
        """
        # Your custom implementation to get unique values for the specified field
        # Example: return MyModel.objects.values_list(field_name, flat=True).distinct()
        return self.model.objects.values_list(field_name, flat=True).distinct()

    def form_select_options(self, field_name: str) -> list:
        """
        Implementation of the form_select_options method.
        """
        # Your custom implementation to get unique values for the specified field
        # Example: return MyModel.objects.values_list(field_name, flat=True).distinct()
        return self.model.objects.values_list(field_name, flat=True).distinct()

    def form_field_type(self, field_name: str) -> str:
        """
        Determine the appropriate form field type for a specific field.

        Parameters:
        - field_name (str): Name of the field for which the form field type is needed.

        Returns:
        str: Form field type for the specified field.

         # Your custom implementation to determine the appropriate form field type # Example: return 'CharField' if
         isinstance(MyModel._meta.get_field(field_name), models.CharField) else 'IntegerField'
        """
        # Get the Django model field instance for the specified field name
        model_field = Artifact._meta.get_field(field_name)

        # Map Django model field types to corresponding form field types
        field_type_mapping = {
            models.CharField: CharField,
            models.IntegerField: IntegerField,
            # Add more mappings as needed for other field types
        }

        # Use the mapping to determine the appropriate form field type
        form_field_type = field_type_mapping.get(type(model_field), CharField)

        # Return the form field type name
        return form_field_type.__name__
