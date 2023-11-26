__author__ = "reed@reedjones.me"
import django_filters
from . import models


#negative filters
class ArtifactFilter(django_filters.Filter):
    uncategorized = django_filters.BooleanFilter(field_name='category', lookup_expr='isnull')


class CategoryChoice(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(
        field_name='category',
        lookup_expr='isnull',
        null_label='Uncategorized',
        queryset=models.Category.objects.all(),
    )
    subcategory = django_filters.ModelChoiceFilter(
        field_name='category__parent'
    )

