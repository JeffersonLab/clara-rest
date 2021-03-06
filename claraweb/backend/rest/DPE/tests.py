# coding=utf-8

import factory
from django.db.models.signals import pre_save, pre_delete

from rest_framework.test import APITestCase


class DPETests(APITestCase):
    fixtures = ['Services.yaml']
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

    @factory.django.mute_signals(pre_save, pre_delete)
    def test_filter_dpe_request_obtains_filtered_data(self):
        response = self.client.get('/dpes/?name=192.')
        self.assertEqual(3, len(response.data))
        response = self.client.get('/dpes/?cores=8')
        self.assertEqual(3, len(response.data))
        response = self.client.get('/dpes/?memory=64')
        self.assertEqual(2, len(response.data))
