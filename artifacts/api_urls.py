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
    # path('states/', api.StateList.as_view(), name='location_list'),
    path('states/<int:pk>/', api.StateDetail.as_view(), name='location_detail'),
    # Add URLs for other views...
    path('artifacts/', ArtifactList.as_view(), name='artifact_list'),
    path('artifacts_simple/', artifacts_list_simple, name='artifacts_list_simple'),
    path('artifacts/<int:pk>/', ArtifactModelDetail.as_view(), name='artifact_detail'),
    path('events/', ProvenanceEventListCreateView.as_view(), name='event_list_create'),
    path('events/<int:pk>/', ProvenanceEventDetailView.as_view(), name='event_detail'),
    path('collections/', CollectionList.as_view(), name='collection_list_create'),
    path('collections/<int:pk>/', CollectionDetail.as_view(), name='collection_detail'),
    path('artifact_master/', ArtifactMasterView.as_view(), name='artifact_master'),

    path('states/', api.StateList.as_view(), name='state_list'),
    path('counties/', api.CountyListView.as_view(), name='county_list'),
    path('regions/', api.RegionListView.as_view(), name='region_list'),
    path('artifact_count_by_type_category/', api.ArtifactCountByTypeCategoryView.as_view(),
         name='artifact_count_by_type_category'),
    path('trades/', TradeList.as_view(), name='trade_list_create'),

    path('trades/<int:pk>/', TradeDetail.as_view(), name='trade_detail'),

]
