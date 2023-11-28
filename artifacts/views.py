from rest_framework.decorators import api_view
from rest_framework.response import Response
from artifacts.models import State, County, Region, Geography, Artifact, Photo, MaterialTag, Attribute, Category, Period, Collection, ArtifactOwnership, ProvenanceEvent, Trade, Person, Date, COA
from artifacts.serializers import StateSerializer, CountySerializer, RegionSerializer, GeographySerializer, ArtifactSerializer, PhotoSerializer, MaterialTagSerializer, AttributeSerializer, CategorySerializer, PeriodSerializer, CollectionSerializer, ArtifactOwnershipSerializer, ProvenanceEventSerializer, TradeSerializer, PersonSerializer, DateSerializer, COASerializer


@api_view(['GET', 'POST'])
def state_list(request):
    if request.method == 'GET':
        items = State.objects.order_by('pk')
        serializer = StateSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def state_detail(request, pk):
    try:
        item = State.objects.get(pk=pk)
    except State.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = StateSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StateSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def county_list(request):
    if request.method == 'GET':
        items = County.objects.order_by('pk')
        serializer = CountySerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CountySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def county_detail(request, pk):
    try:
        item = County.objects.get(pk=pk)
    except County.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = CountySerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CountySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def region_list(request):
    if request.method == 'GET':
        items = Region.objects.order_by('pk')
        serializer = RegionSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RegionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def region_detail(request, pk):
    try:
        item = Region.objects.get(pk=pk)
    except Region.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = RegionSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RegionSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def geography_list(request):
    if request.method == 'GET':
        items = Geography.objects.order_by('pk')
        serializer = GeographySerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = GeographySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def geography_detail(request, pk):
    try:
        item = Geography.objects.get(pk=pk)
    except Geography.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = GeographySerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GeographySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def artifact_list(request):
    if request.method == 'GET':
        items = Artifact.objects.order_by('pk')
        serializer = ArtifactSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArtifactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def artifact_detail(request, pk):
    try:
        item = Artifact.objects.get(pk=pk)
    except Artifact.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = ArtifactSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArtifactSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def photo_list(request):
    if request.method == 'GET':
        items = Photo.objects.order_by('pk')
        serializer = PhotoSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def photo_detail(request, pk):
    try:
        item = Photo.objects.get(pk=pk)
    except Photo.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = PhotoSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PhotoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def materialtag_list(request):
    if request.method == 'GET':
        items = MaterialTag.objects.order_by('pk')
        serializer = MaterialTagSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MaterialTagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def materialtag_detail(request, pk):
    try:
        item = MaterialTag.objects.get(pk=pk)
    except MaterialTag.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = MaterialTagSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MaterialTagSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def attribute_list(request):
    if request.method == 'GET':
        items = Attribute.objects.order_by('pk')
        serializer = AttributeSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AttributeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def attribute_detail(request, pk):
    try:
        item = Attribute.objects.get(pk=pk)
    except Attribute.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = AttributeSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AttributeSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        items = Category.objects.order_by('pk')
        serializer = CategorySerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    try:
        item = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = CategorySerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CategorySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def period_list(request):
    if request.method == 'GET':
        items = Period.objects.order_by('pk')
        serializer = PeriodSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PeriodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def period_detail(request, pk):
    try:
        item = Period.objects.get(pk=pk)
    except Period.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = PeriodSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PeriodSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        items = Collection.objects.order_by('pk')
        serializer = CollectionSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    try:
        item = Collection.objects.get(pk=pk)
    except Collection.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = CollectionSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CollectionSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def artifactownership_list(request):
    if request.method == 'GET':
        items = ArtifactOwnership.objects.order_by('pk')
        serializer = ArtifactOwnershipSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArtifactOwnershipSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def artifactownership_detail(request, pk):
    try:
        item = ArtifactOwnership.objects.get(pk=pk)
    except ArtifactOwnership.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = ArtifactOwnershipSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArtifactOwnershipSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def provenanceevent_list(request):
    if request.method == 'GET':
        items = ProvenanceEvent.objects.order_by('pk')
        serializer = ProvenanceEventSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProvenanceEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def provenanceevent_detail(request, pk):
    try:
        item = ProvenanceEvent.objects.get(pk=pk)
    except ProvenanceEvent.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = ProvenanceEventSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProvenanceEventSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def trade_list(request):
    if request.method == 'GET':
        items = Trade.objects.order_by('pk')
        serializer = TradeSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TradeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def trade_detail(request, pk):
    try:
        item = Trade.objects.get(pk=pk)
    except Trade.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = TradeSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TradeSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def person_list(request):
    if request.method == 'GET':
        items = Person.objects.order_by('pk')
        serializer = PersonSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def person_detail(request, pk):
    try:
        item = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = PersonSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PersonSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def date_list(request):
    if request.method == 'GET':
        items = Date.objects.order_by('pk')
        serializer = DateSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def date_detail(request, pk):
    try:
        item = Date.objects.get(pk=pk)
    except Date.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = DateSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DateSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def coa_list(request):
    if request.method == 'GET':
        items = COA.objects.order_by('pk')
        serializer = COASerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = COASerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def coa_detail(request, pk):
    try:
        item = COA.objects.get(pk=pk)
    except COA.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = COASerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = COASerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)
