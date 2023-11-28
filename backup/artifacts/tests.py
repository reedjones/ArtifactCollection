from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse

from . models import Artifact
from . forms import ArtifactForm


class ArtifactAPITestCase(TestCase):
    def test_get_artifact_list(self):
        response = self.client.get(reverse('artifact-list'))
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on your API logic

class ArtifactFormTestCase(TestCase):
    def test_artifact_form_valid(self):
        form_data = {'name': 'Test Artifact', }
        form = ArtifactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_artifact_form_invalid(self):
        form_data = {'name': ''}
        form = ArtifactForm(data=form_data)
        self.assertFalse(form.is_valid())

class ArtifactDetailViewTestCase(TestCase):
    def setUp(self):
        self.artifact = Artifact.objects.create(name="Test Artifact")

    def test_artifact_detail_view(self):
        response = self.client.get(reverse('artifact_detail', args=[self.artifact.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.artifact.name)
        # Add more assertions based on your view logic



class ArtifactModelTestCase(TestCase):
    def test_create_artifact(self):
        artifact = Artifact.objects.create(name="Test Artifact")
        self.assertEqual(artifact.name, "Test Artifact")
        # Add more assertions based on your model fields and logic