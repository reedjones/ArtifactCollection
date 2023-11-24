__author__ = "reed@reedjones.me"
from rest_framework import serializers
from .models import (
    Artifact, MaterialTag, Category,
    Period, Collection, ArtifactOwnership, Trade,
    Person, Date, COA, Photo, State, County, Region, ProvenanceEvent
)

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('name', 'description')

class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = ('name', 'description', 'state')



class ArtifactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artifact
        fields = '__all__'

class MaterialTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialTag
        fields = '__all__'



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class CollectionSerializer(serializers.ModelSerializer):
    owner = PersonSerializer()

    class Meta:
        model = Collection
        fields = '__all__'

class ArtifactOwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtifactOwnership
        fields = '__all__'

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'



class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = '__all__'

class COASerializer(serializers.ModelSerializer):
    class Meta:
        model = COA
        fields = '__all__'

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'



class ProvenanceEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvenanceEvent
        fields = '__all__'

