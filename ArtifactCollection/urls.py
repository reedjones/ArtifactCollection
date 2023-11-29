"""
URL configuration for ArtifactCollection project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

from ArtifactCollection.views import PDFReportView


def home(request):
    return render(request, 'homepage.html', {

    })


def home2(request):
    return render(request, 'homepage2.html', {

    })


urlpatterns = [
    # path('grappelli/', include('grappelli.urls')),  # grappelli URLS
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # <-- And here

    path("admin/", admin.site.urls),
    path('artifacts-api/', include('artifacts.api_urls')),  # Replace 'yourapp' with your app name
    path('api-service/', include('data_service.urls')),
    path('pdf-report/', PDFReportView.as_view(), name='pdf-report'),
    path('accounts/', include('allauth.urls')),  # Add this line
    path('docs/', include_docs_urls(title='My API service'), name='api-docs'),

    path('core/', include('core.urls'), name='core'),

    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things …"
    ), name='openapi-schema'),
    path('', home, name='home'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]

print(settings.DEBUG)

if settings.DEBUG:
    print("updating settings")
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        # ...
        path("__debug__/", include("debug_toolbar.urls")),
    ]
