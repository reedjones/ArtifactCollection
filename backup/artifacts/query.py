__author__ = "reed@reedjones.me"
from . import models
from django.db.models import Count, F, OuterRef, Subquery, Q

from .models import ProvenanceEvent, Artifact, Photo


def artifacts_involved_in_trades():
    return Artifact.objects.filter(Q(trade__from_collection__isnull=False) | Q(trade__to_collection__isnull=False)).with_related('category', 'geography').prefetch_related('photos__photo_type', 'materials')


# In your query helpers module
def artifacts_with_optimized_certifications():
    return Artifact.objects.with_related('category', 'geography').prefetch_related('photos__photo_type', 'materials', 'artifactownership__certification__signer')


# In your query helpers module
def artifacts_with_optimized_certifications():
    return Artifact.objects.with_related('category', 'geography').prefetch_related('photos__photo_type', 'materials', 'artifactownership__certification__signer')



# In your query helpers module
def artifacts_with_certifications():
    return Artifact.objects.with_related('category', 'geography').prefetch_related('photos__photo_type', 'materials', 'artifactownership__certification__signer')


# In your query helpers module
def artifacts_categorized_by_period_optimized():
    return Artifact.objects.annotate(
        period_name=F('period__name'),
        period_date_range=F('period__date_range')
    ).with_related('category', 'geography').prefetch_related('photos__photo_type', 'materials')



# In your query helpers module
def artifacts_categorized_by_period():
    return Artifact.objects.annotate(
        period_name=F('period__name'),
        period_date_range=F('period__date_range')
    ).with_related('category', 'geography').prefetch_related('photos__photo_type', 'materials')



# In your query helpers module
def artifacts_in_collection(collection_id):
    return Artifact.objects.filter(artifactownership__collection_id=collection_id).with_related('category', 'geography').prefetch_related('photos__photo_type', 'materials')



# In your query helpers module
def artifacts_owned_by_person(person_id):
    return Artifact.objects.filter(artifactownership__owner_id=person_id).with_related('category', 'geography').prefetch_related('photos__photo_type', 'materials')



# In your query helpers module
def provenance_events_for_artifact_ordered(artifact_id):
    return ProvenanceEvent.objects.filter(artifact_id=artifact_id).order_by('date', 'created_at')


# In your query helpers module
def provenance_events_for_artifact(artifact_id):
    return ProvenanceEvent.objects.filter(artifact_id=artifact_id).order_by('date')



# In your query helpers module
def artifacts_with_optimized_materials():
    return Artifact.objects.with_materials().with_related('category', 'geography').prefetch_related('photos__photo_type', 'materials')


# In your query helpers module
def artifacts_with_materials():
    return Artifact.objects.with_materials().with_related('category', 'geography').prefetch_related('photos__photo_type')



# In your query helpers module
def artifacts_with_detailed_photos():
    main_photo_subquery = Photo.objects.filter(
        artifact=OuterRef('pk')
    ).order_by('pk').values('filename')[:1]
    qs = Artifact.objects.with_related('category', 'geography').prefetch_related('photos__photo_type', 'materials').annotate(
        photo_url=Subquery(main_photo_subquery),
        photo_count=Count('photos'),
        subcategory=F('category__parent__name'),
        maincategory=F('category__name'),
        category_attribute=F('category__attribute__name'),
        from_state=F('geography__state__name')
    )
    return qs



# In your query helpers module
def artifacts_with_most_photos():
    return Artifact.objects.with_photos().annotate(photo_count=Count('photos')).order_by('-photo_count').with_related('category', 'geography').prefetch_related('photos__photo_type', 'materials')



# In your query helpers module
def artifacts_by_state_optimized(state_name):
    return Artifact.objects.filter(geography__state__name=state_name).with_materials().prefetch_related('photos__photo_type', 'materials')

def artifacts_by_region_optimized(region_name):
    return Artifact.objects.filter(geography__region__name=region_name).with_materials().prefetch_related('photos__photo_type', 'materials')

def artifacts_by_county_optimized(county_name):
    return Artifact.objects.filter(geography__county__name=county_name).with_materials().prefetch_related('photos__photo_type', 'materials')



# In your query helpers module
def artifacts_by_state(state_name):
    return Artifact.objects.filter(geography__state__name=state_name).with_materials()

def artifacts_by_region(region_name):
    return Artifact.objects.filter(geography__region__name=region_name).with_materials()

def artifacts_by_county(county_name):
    return Artifact.objects.filter(geography__county__name=county_name).with_materials()


# In your query helpers module
from django.db.models import Avg

def category_analysis():
    return Artifact.objects.values('category__name').annotate(
        artifact_count=Count('id'),
        avg_condition=Avg('condition')
    )



# In your query helpers module


def artifact_count_by_category():
    return Artifact.objects.values('category__name').annotate(artifact_count=Count('id'))


# In your query helpers module
def artifacts_with_details():
    return Artifact.objects.with_photos_and_categories().with_related('finder', 'geography', 'category')


# In your query helpers module
def artifacts_with_optimized_details():
    return Artifact.objects.with_photos_and_categories().with_related('finder', 'geography', 'category').prefetch_related('photos__photo_type', 'materials')

