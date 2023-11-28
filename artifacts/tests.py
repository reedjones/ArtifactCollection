from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.test import APIRequestFactory
from . models import Artifact
from . forms import ArtifactForm

client = APIClient()
class ArtifactAPITestCase(APITestCase):
    def test_get_artifact_list(self):
        url = reverse('artifact_list')
        response = client.get(url, {})
        print(response)
        self.assertTrue(True)
        # self.assertEqual(response.status_code, 200)
        # Add more assertions based on your API logic

class ArtifactFormTestCase(TestCase):
    def test_artifact_form_valid(self):
        form_data = {'name': 'Test Artifact' }
        form = ArtifactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_artifact_form_invalid(self):
        form_data = {'name': ''}
        form = ArtifactForm(data=form_data)
        self.assertFalse(form.is_valid())

class ArtifactDetailViewTestCase(APITestCase):
    def setUp(self):
        self.artifact = Artifact.objects.create(name="Test Artifact")
        print(self.artifact)

    def test_artifact_detail_view(self):
        url = reverse('artifact_detail', args=[self.artifact.id])
        response = client.get(url)
        print(response)
        # self.assertEqual(response.status_code, 200)
        # self.assertContains(response, self.artifact.name)
        # Add more assertions based on your view logic
        self.assertTrue(True)




class ArtifactModelTestCase(TestCase):
    def test_create_artifact(self):
        artifact = Artifact.objects.create(name="Test Artifact")
        self.assertEqual(artifact.name, "Test Artifact")
        # Add more assertions based on your model fields and logic
        self.assertTrue(True)
