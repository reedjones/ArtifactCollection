from rest_framework.serializers import ModelSerializer
from artifacts.models import (
    State, County, Region, Geography, Artifact, Photo,
    MaterialTag, Attribute,
    Category, Period, Collection, ArtifactOwnership,
    ProvenanceEvent, Trade, Person, Date, COA
)


class StateSerializer(ModelSerializer):

    class Meta:
        model = State
        depth = 2
        fields = '__all__'


class CountySerializer(ModelSerializer):

    class Meta:
        model = County
        depth = 2
        fields = '__all__'


class RegionSerializer(ModelSerializer):

    class Meta:
        model = Region
        depth = 2
        fields = '__all__'


class GeographySerializer(ModelSerializer):

    class Meta:
        model = Geography
        depth = 2
        fields = '__all__'


class ArtifactSerializer(ModelSerializer):

    class Meta:
        model = Artifact
        depth = 2
        fields = '__all__'


class PhotoSerializer(ModelSerializer):

    class Meta:
        model = Photo
        depth = 2
        fields = '__all__'


class MaterialTagSerializer(ModelSerializer):

    class Meta:
        model = MaterialTag
        depth = 2
        fields = '__all__'


class AttributeSerializer(ModelSerializer):

    class Meta:
        model = Attribute
        depth = 2
        fields = '__all__'


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        depth = 2
        fields = '__all__'


class PeriodSerializer(ModelSerializer):

    class Meta:
        model = Period
        depth = 2
        fields = '__all__'


class CollectionSerializer(ModelSerializer):

    class Meta:
        model = Collection
        depth = 2
        fields = '__all__'


class ArtifactOwnershipSerializer(ModelSerializer):

    class Meta:
        model = ArtifactOwnership
        depth = 2
        fields = '__all__'


class ProvenanceEventSerializer(ModelSerializer):

    class Meta:
        model = ProvenanceEvent
        depth = 2
        fields = '__all__'


class TradeSerializer(ModelSerializer):

    class Meta:
        model = Trade
        depth = 2
        fields = '__all__'


class PersonSerializer(ModelSerializer):

    class Meta:
        model = Person
        depth = 2
        fields = '__all__'


class DateSerializer(ModelSerializer):

    class Meta:
        model = Date
        depth = 2
        fields = '__all__'


class COASerializer(ModelSerializer):

    class Meta:
        model = COA
        depth = 2
        fields = '__all__'



