# coding=utf-8

from rest_framework import status
from rest_framework.test import APITestCase


class DPETests(APITestCase):
    fixtures = ['claraweb/web_backend/tests/fixtures/Services.yaml']
    url = '/dpes/'
    url_del = url+'2'

    initial_data = {
      "language": "java",
      "start_time": "2015-09-25T11:33:21.783",
      "hostname": "1.1.1.21",
      "modified": "2015-09-29T16:29:27.711",
      "n_cores": 24,
      "memory_size": 64
    }

    def test_create_node(self):
        """
        We must ensure that the DPE node instance gets created
        correctly into the database
        """
        response = self.client.post(self.url, self.initial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_node(self):
        """
        We must ensure that the DPE node instance gets deleted
        correctly into the database under delete request
        """
        response = self.client.delete(self.url_del, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_dpe_request_obtains_filtered_data(self):
        response = self.client.get('/dpes/?filter_by_name=192.')
        self.assertEqual(3, len(response.data))
        response = self.client.get('/dpes/?filter_by_cores=8')
        self.assertEqual(3, len(response.data))
        response = self.client.get('/dpes/?filter_by_memory=64')
        self.assertEqual(2, len(response.data))
        response = self.client.get('/dpes/?filter_by_containername=abc')
        self.assertEqual(2, len(response.data))
        response = self.client.get('/dpes/?filter_by_servicename=super')
        self.assertEqual(3, len(response.data))
