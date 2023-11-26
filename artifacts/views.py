from django.shortcuts import render
from django.views.generic import TemplateView
# views.py
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from django.views import View
from django.db.models import Count, Sum, Avg
from .models import Artifact

# Create your views here.


class StateCountyFilterView(TemplateView):
    template_name = 'artifacts/state_filter.html'



