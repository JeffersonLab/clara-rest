'''
Created on 26-03-2015

@author: royarzun
'''
from rest_framework import status
from rest_framework.test import APITestCase


class DPENodeTests(APITestCase):
    fixtures = ['fixtures/Nodes.yaml',]
    url = '/dpes/'
    url_put = url+'2'
    url_del = url+'4'
    initial_data = {'hostname':'127.0.0.1'}
    
    
    def test_create_node(self):
        '''
        We must ensure that the DPE node instance gets created
        correctly into the database
        '''
        response = self.client.post(self.url, self.initial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_update_node(self):
        '''
        We must ensure that the DPE node instance gets updated
        correctly into the database
        '''
        updated_data = {"hostname" : "192.168.1.254"}
        response = self.client.put(self.url_put, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_delete_node(self):
        '''
        We must ensure that the DPE node instance gets deleted
        correctly into the database under delete request
        '''
        response = self.client.delete(self.url_del, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
