from django.urls import re_path as path
from rest_framework.urlpatterns import format_suffix_patterns
from artifacts import views


url_patterns= [
    path(r'^state/(?P<pk>[0-9]+)/$', views.state_detail),
    path(r'^state/$', views.state_list),

    path(r'^county/(?P<pk>[0-9]+)/$', views.county_detail),
    path(r'^county/$', views.county_list),

    path(r'^region/(?P<pk>[0-9]+)/$', views.region_detail),
    path(r'^region/$', views.region_list),

    path(r'^geography/(?P<pk>[0-9]+)/$', views.geography_detail),
    path(r'^geography/$', views.geography_list),

    path(r'^artifact/(?P<pk>[0-9]+)/$', views.artifact_detail),
    path(r'^artifact/$', views.artifact_list),

    path(r'^photo/(?P<pk>[0-9]+)/$', views.photo_detail),
    path(r'^photo/$', views.photo_list),

    path(r'^materialtag/(?P<pk>[0-9]+)/$', views.materialtag_detail),
    path(r'^materialtag/$', views.materialtag_list),

    path(r'^attribute/(?P<pk>[0-9]+)/$', views.attribute_detail),
    path(r'^attribute/$', views.attribute_list),

    path(r'^category/(?P<pk>[0-9]+)/$', views.category_detail),
    path(r'^category/$', views.category_list),

    path(r'^period/(?P<pk>[0-9]+)/$', views.period_detail),
    path(r'^period/$', views.period_list),

    path(r'^collection/(?P<pk>[0-9]+)/$', views.collection_detail),
    path(r'^collection/$', views.collection_list),

    path(r'^artifactownership/(?P<pk>[0-9]+)/$', views.artifactownership_detail),
    path(r'^artifactownership/$', views.artifactownership_list),

    path(r'^provenanceevent/(?P<pk>[0-9]+)/$', views.provenanceevent_detail),
    path(r'^provenanceevent/$', views.provenanceevent_list),

    path(r'^trade/(?P<pk>[0-9]+)/$', views.trade_detail),
    path(r'^trade/$', views.trade_list),

    path(r'^person/(?P<pk>[0-9]+)/$', views.person_detail),
    path(r'^person/$', views.person_list),

    path(r'^date/(?P<pk>[0-9]+)/$', views.date_detail),
    path(r'^date/$', views.date_list),

    path(r'^coa/(?P<pk>[0-9]+)/$', views.coa_detail),
    path(r'^coa/$', views.coa_list),

]

pathpatterns = format_suffix_patterns(url_patterns)
