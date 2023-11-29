__author__ = "reed@reedjones.me"
# forms.py

from django import forms
from core.models import UserProfile

class UserProfileForm(forms.ModelForm):
    pass
    # class Meta:
    #     model = UserProfile
    #     fields = ['field1', 'field2', 'field3']  # Include the fields you want to allow users to edit
