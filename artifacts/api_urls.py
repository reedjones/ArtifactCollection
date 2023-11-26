__author__ = "reed@reedjones.me"
__author__ = "reed@reedjones.me"

from django.urls import path

from . import api
from .api import (
    ArtifactList, ArtifactModelDetail,
    ProvenanceEventListCreateView, ProvenanceEventDetailView,
    CollectionList, CollectionDetail, TradeList, TradeDetail, ArtifactMasterView, artifacts_list_simple
)

urlpatterns = [
    # path('states/', api.StateList.as_view(), name='location-list'),
    path('states/<int:pk>/', api.StateDetail.as_view(), name='location-detail'),
    # Add URLs for other views...
    path('artifacts/', ArtifactList.as_view(), name='artifact-model-list'),
    path('artifacts-simple/', artifacts_list_simple, name='artifacts_list_simple'),
    path('artifacts/<int:pk>/', ArtifactModelDetail.as_view(), name='artifact-model-detail'),
    path('events/', ProvenanceEventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', ProvenanceEventDetailView.as_view(), name='event-detail'),
    path('collections/', CollectionList.as_view(), name='collection-list-create'),
    path('collections/<int:pk>/', CollectionDetail.as_view(), name='collection-detail'),
    path('artifact-master/', ArtifactMasterView.as_view(), name='artifact_master'),

    path('states/', api.StateList.as_view(), name='state_list'),
    path('counties/', api.CountyListView.as_view(), name='county_list'),
    path('regions/', api.RegionListView.as_view(), name='region_list'),
    path('artifact-count-by-type-category/', api.ArtifactCountByTypeCategoryView.as_view(),
         name='artifact_count_by_type_category'),
    path('trades/', TradeList.as_view(), name='trade-list-create'),

    path('trades/<int:pk>/', TradeDetail.as_view(), name='trade-detail'),

]
