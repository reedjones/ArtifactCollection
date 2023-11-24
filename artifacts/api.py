__author__ = "reed@reedjones.me"


from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import State, ProvenanceEvent
from .models import (
    Artifact, MaterialTag, Category,
    Period, Collection, ArtifactOwnership, Trade,
    Person, Date, COA, Photo
)
from .serializers import StateSerializer, ProvenanceEventSerializer
from rest_framework.decorators import api_view, permission_classes
from .serializers import (
    ArtifactSerializer, MaterialTagSerializer,
    CategorySerializer, PeriodSerializer, CollectionSerializer,
    ArtifactOwnershipSerializer, TradeSerializer, PersonSerializer,
    DateSerializer, COASerializer, PhotoSerializer
)


@api_view(['GET'])
@permission_classes([AllowAny])
def example_view(request, format=None):
    content = {
        'status': 'request was permitted'
    }
    return Response(content)


class StateList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = State.objects.all()
    serializer_class = StateSerializer





class StateDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = State.objects.all()
    serializer_class = StateSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)




class AwImageSpecDetail(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PhotoList(generics.ListCreateAPIView):
    queryset = Photo.objects.all()
    permission_classes = [AllowAny]
    serializer_class = PhotoSerializer


class COADetail(generics.RetrieveUpdateDestroyAPIView):

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class COAList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = COA.objects.all()
    serializer_class = COASerializer

class DateDetail(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class DateList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Date.objects.all()
    serializer_class = DateSerializer

class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class PersonList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class TradeDetail(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class TradeList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer

class ArtifactOwnershipDetail(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class ArtifactOwnershipList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArtifactOwnershipSerializer
    queryset = ArtifactOwnership.objects.all()

class CollectionDetail(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CollectionList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()

class PeriodDetail(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class PeriodList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer

class TypeCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CategoryList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer





class MaterialTagDetail(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class MaterialTagList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = MaterialTagSerializer
    queryset = MaterialTag.objects.all()

class ArtifactModelDetail(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class ArtifactList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Artifact.objects.all()
    serializer_class = ArtifactSerializer


class ProvenanceEventListCreateView(generics.ListCreateAPIView):
    queryset = ProvenanceEvent.objects.all()
    serializer_class = ProvenanceEventSerializer

class ProvenanceEventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProvenanceEvent.objects.all()
    serializer_class = ProvenanceEventSerializer