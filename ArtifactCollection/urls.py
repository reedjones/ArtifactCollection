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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from ArtifactCollection.views import PDFReportView
from django.shortcuts import render
def home(request):
    return render(request, 'homepage2.html', {

    })

urlpatterns = [
    # path('grappelli/', include('grappelli.urls')),  # grappelli URLS

    path("admin/", admin.site.urls),
    path('artifacts-api/', include('artifacts.api_urls')),  # Replace 'yourapp' with your app name
    path('api-service/', include('data_service.urls')),
    path('pdf-report/', PDFReportView.as_view(), name='pdf-report'),
    path('accounts/', include('allauth.urls')),  # Add this line

    path('', home, name='home')

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