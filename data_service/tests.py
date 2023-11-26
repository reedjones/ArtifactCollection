__author__ = "reed@reedjones.me"
# tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient





import logging
import sys
from autologging import logged, TRACE, traced

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout,format="HIHIH%(levelname)s:%(filename)s,%(lineno)d:%(name)s.%(funcName)s:%(message)s")

@traced
class DataServiceAPITest(TestCase):
    def setUp(self):
        super(DataServiceAPITest, self).setUp()
        self.client = APIClient(

        )
        self.url = reverse('data-service-api')


    # def test_data_service_api(self):
    #     url = reverse('data-service-api')
    #     client = APIClient()
    #
    #     # Prepare a payload for the DataServiceAPIView
    #     payload = {
    #         "model_name": "Artifact",
    #         "method_name": "get_model_info",
    #         "what": "category__name",
    #         "value": "Field2",
    #         "aggregation": "Sum"
    #     }
    #
    #     response = client.post(url, data=payload, format='json')
    #
    #     # Assert that the response is successful and contains the expected result
    #     print(response)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['result'], 'success')
    #     self.assertIn('Result for Field1, Field2, Field3', response.data['data'])

    def test_get_service_options(self):
        response = self.client.get(self.url, {}, format='json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @logged
    def test_get_field_choices(self):
        # data_service.get_field_choices('name')
        payload = {
            'method_name':'get_field_choices',
            'model_name':'Category',
            'field_name':'name'
        }
        response = self.client.post(self.url, payload, format='json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

