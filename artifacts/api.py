__author__ = "reed@reedjones.me"

from django.core.paginator import Paginator, EmptyPage
from django.db.models import Count, Sum, Avg
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.views.generic import View
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import (
    Artifact, MaterialTag, Category,
    Period, Collection, ArtifactOwnership, Trade,
    Person, Date, COA, Photo, Region
)
from .models import ProvenanceEvent
from .models import State, County
from .serializers import (
    ArtifactSerializer, MaterialTagSerializer,
    CategorySerializer, PeriodSerializer, CollectionSerializer,
    ArtifactOwnershipSerializer, TradeSerializer, PersonSerializer,
    DateSerializer, COASerializer, PhotoSerializer
)
from .serializers import StateSerializer, ProvenanceEventSerializer

from django.db.models import CharField, Value as V



class StateList(View):
    def get(self, request, *args, **kwargs):
        states = State.objects.all().annotate(flag=
                                            Concat(V("/static/flags/Flag_of_"), "name", V(".svg"),
                                                   output_field=CharField())).values('id', 'name', 'flag')
        return JsonResponse({'states': list(states)})



class StateList2(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = State.objects.all()
    serializer_class = StateSerializer

class CountyListView(View):
    def get(self, request, *args, **kwargs):
        counties = County.objects.all()
        state_id = request.GET.get('state_id', None)
        if state_id:
            counties = counties.filter(state_id=state_id)
        return JsonResponse({'counties': list(counties.values('id', 'name'))})


@api_view(['GET'])
@permission_classes([AllowAny])
def example_view(request, format=None):
    content = {
        'status': 'request was permitted'
    }
    return Response(content)



class StateDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = State.objects.all()
    serializer_class = StateSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AwImageSpecDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PhotoSerializer
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PhotoList(generics.ListCreateAPIView):
    queryset = Photo.objects.all()
    permission_classes = [AllowAny]
    serializer_class = PhotoSerializer


class COADetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = COASerializer
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class COAList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = COA.objects.all()
    serializer_class = COASerializer


class DateDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DateSerializer
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class DateList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Date.objects.all()
    serializer_class = DateSerializer


class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PersonSerializer
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PersonList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class TradeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TradeSerializer
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TradeList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer


class ArtifactOwnershipDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArtifactOwnershipSerializer
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ArtifactOwnershipList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArtifactOwnershipSerializer
    queryset = ArtifactOwnership.objects.all()


class CollectionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CollectionSerializer
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CollectionList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()


class PeriodDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PeriodSerializer
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PeriodList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer


class TypeCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
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
    serializer_class = ArtifactSerializer

    def get(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        instance =  Artifact.objects.get(pk=pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_class(self, *args, **kwargs):
        return ArtifactSerializer


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


class RegionListView(View):
    def get(self, request, *args, **kwargs):
        regions = Region.objects.all()
        state_id = request.GET.get('state_id', None)
        if state_id:
            regions = regions.filter(state_id=state_id)
        return JsonResponse({'counties': list(regions.values('id', 'name'))})


class MaterialListView(View):
    def get(self, request, *args, **kwargs):
        mats = MaterialTag.objects.all()
        artifact = request.GET.get('artifact_id', None)
        state_id = request.GET.get('state_id', None)
        if artifact:
            mats = mats.filter(artifact=artifact)
        if state_id:
            mats = mats.filter(artifact__state=state_id)

        return JsonResponse({'counties': list(mats.values('id', 'name'))})


class PersonListView(View):
    def get(self, request, *args, **kwargs):
        people = Person.objects.all()
        collection_id = request.GET.get('collection_id', None)
        artifact_id = request.GET.get('artifact_id', None)
        event_id = request.GEt.get('event_id', None)
        if collection_id:
            people = people.filter(collection=collection_id)
        return JsonResponse({'counties': list(people.values('id', 'name'))})


class ArtifactCountByTypeCategoryView(View):
    def get(self, request, *args, **kwargs):
        # Perform aggregation using Django's ORM
        artifact_counts = Artifact.objects.values('type_category__name', 'material_tag__name') \
            .annotate(count=Count('id'))

        # Convert queryset to list for JSON serialization
        artifact_counts_list = list(artifact_counts)

        return JsonResponse({'artifact_counts': artifact_counts_list})


def artifacts_list_simple(request):
    # Apply order_by
    qs = Artifact.objects.with_photos_and_categories()
    order_by = request.GET.get('order_by', 'id')
    queryset = qs.order_by(order_by)

    # Apply pagination
    page = request.GET.get('page', 1)
    per_page = int(request.GET.get('per_page', 10))
    paginator = Paginator(queryset, per_page)  # Adjust the page size as needed
    try:
        page_data = paginator.page(page)
    except EmptyPage:
        return JsonResponse({'error': 'Invalid page number'})

    artifact_data = page_data.object_list
    data_count = artifact_data.count()
    data_list = list(  # Only fetch the values we need
        artifact_data.values(
            'aw_item_number',
            'photo_url',
            'subcategory',
            'maincategory',
            'category_attribute',
            'from_state',
            'id')
    )

    return JsonResponse(
        {'artifacts': data_list,
         'pagination': {
             'total_pages': paginator.num_pages,
             'current_page': page,
             'objects_count': data_count,
             'per_page': per_page
         }
         }
    )


class ArtifactMasterView(View):
    def get(self, request, *args, **kwargs):
        aggregation = request.GET.get('aggregation', None)
        filter_type_category = request.GET.get('filter_type_category', None)
        filter_material_tag = request.GET.get('filter_material_tag', None)

        # Build base queryset
        queryset = Artifact.objects.all()

        # Apply filters if provided
        if filter_type_category:
            queryset = queryset.filter(type_category__name=filter_type_category)

        if filter_material_tag:
            queryset = queryset.filter(material_tag__name=filter_material_tag)

        # Apply aggregation if provided
        if aggregation:
            if aggregation == 'count':
                result = queryset.count()
            elif aggregation == 'sum':
                result = queryset.aggregate(Sum('some_numeric_field'))['some_numeric_field__sum']
            elif aggregation == 'average':
                result = queryset.aggregate(Avg('some_numeric_field'))['some_numeric_field__avg']
            else:
                return JsonResponse({'error': 'Invalid aggregation parameter'})

            return JsonResponse({'result': result})

        # Fetch additional parameters
        order_by = request.GET.get('order_by', 'id')
        page = request.GET.get('page', 1)

        # Apply order_by
        queryset = queryset.order_by(order_by)

        # Apply pagination
        paginator = Paginator(queryset, 10)  # Adjust the page size as needed
        try:
            page_data = paginator.page(page)
        except EmptyPage:
            return JsonResponse({'error': 'Invalid page number'})

        artifact_data = list(page_data.object_list.values())

        return JsonResponse(
            {'artifacts': artifact_data, 'pagination': {'total_pages': paginator.num_pages, 'current_page': page}})
