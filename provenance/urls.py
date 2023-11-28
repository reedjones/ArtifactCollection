__author__ = "reed@reedjones.me"
from django.urls import path
from . import views

urlpatterns = [
    path('timelines/', views.artifact_timelines, name="timeline_list"),
    path('timeline/detail/<int:pk>/', views.timeline_detail, 'timeline_detail'),
    path('coas/', views.certifications, name='certification_list'),
    path('coa/detail/<int:pk>/', views.certification_detail, name='certification_detail'),



]