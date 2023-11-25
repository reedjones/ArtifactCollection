
from django.urls import path

from .views import view_profile, edit_profile, change_password

urlpatterns = [
    path('profile/', view_profile, name='view_profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/change-password/', change_password, name='change_password'),
    # Add other profile-related URLs as needed
]