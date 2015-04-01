'''
Created on 26-03-2015

@author: royarzun
'''
from rest_framework import status
from rest_framework.test import APITestCase


class DPENodeTests(APITestCase):
    fixtures = ['fixtures/Nodes.yaml', ]
    url = '/dpes/'
    url_del = url+'4'
    initial_data = {'DPEInfo': 2}

    def test_create_node(self):
        '''
        We must ensure that the DPE node instance gets created
        correctly into the database
        '''
        print "\n- Testing Node create DPEs method"
        response = self.client.post(self.url, self.initial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_node(self):
        '''
        We must ensure that the DPE node instance gets deleted
        correctly into the database under delete request
        '''
        print "\n- Testing Node delete method"
        response = self.client.delete(self.url_del, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
