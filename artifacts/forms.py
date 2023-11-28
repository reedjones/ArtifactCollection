__author__ = "reed@reedjones.me"
from django import forms
from .models import Artifact

class ArtifactForm(forms.ModelForm):
    class Meta:
        model = Artifact
        fields = ['name']