__author__ = "reed@reedjones.me"
__author__ = "reed@reedjones.me"

from django.urls import path

from . import api
from .api import (
    ArtifactList, ArtifactModelDetail,
    ProvenanceEventListCreateView, ProvenanceEventDetailView,
CollectionList, CollectionDetail, TradeList, TradeDetail
)

urlpatterns = [
    path('states/', api.StateList.as_view(), name='location-list'),
    path('states/<int:pk>/', api.StateDetail.as_view(), name='location-detail'),
    # Add URLs for other views...
    path('artifact-models/', ArtifactList.as_view(), name='artifact-model-list'),
    path('artifact-models/<int:pk>/', ArtifactModelDetail.as_view(), name='artifact-model-detail'),
path('api/events/', ProvenanceEventListCreateView.as_view(), name='event-list-create'),
    path('api/events/<int:pk>/', ProvenanceEventDetailView.as_view(), name='event-detail'),
    path('collections/', CollectionListCreateView.as_view(), name='collection-list-create'),
    path('collections/<int:pk>/', CollectionDetailView.as_view(), name='collection-detail'),

    path('trades/', TradeListCreateView.as_view(), name='trade-list-create'),
    path('trades/<int:pk>/', TradeDetailView.as_view(), name='trade-detail'),

]
