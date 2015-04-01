'''
Created on 27-03-2015

@author: royarzun
'''
from rest_framework import status
from rest_framework.test import APITestCase


class ContainerTests(APITestCase):
    fixtures = ['fixtures/Nodes.yaml', 'fixtures/Container.yaml']
    url_nested = '/dpes/2/containers/'
    url_container = '/containers/'
    url_del = url_nested+'5'
    initial_data = {'name': 'abc', 'dpe_id': '2'}

    def test_create_node_container(self):
        '''
        We must ensure that the container instance gets created
        correctly into the database
        '''
        print "\n- Testing Node/Container create method"
#         response = self.client.post(self.url_nested,
#                                     self.initial_data,
#                                     format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pass

    def test_delete_node_container(self):
        '''
        We must ensure that the container instance gets deleted
        correctly into the database under delete request
        '''
        print "\n- Testing Node/Container delete method"
#         response = self.client.delete(self.url_del, format='json')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        pass

    def test_create_container(self):
        '''
        We must ensure that the container instance gets created
        correctly into the database
        '''
        print "\n- Testing Container create method"
#         container_data = {'name': 'abcdefghijk', 'dpe_id': '2'}
#         response = self.client.post(self.url_container,
#                                     container_data,
#                                     format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pass

    def test_delete_container(self):
        '''
        We must ensure that the container instance gets deleted
        correctly into the database under delete request
        '''
        print "\n- Testing Container delete method"
        pass
