# coding=utf-8

from rest_framework import status
from rest_framework.test import APITestCase


class ContainerTests(APITestCase):
    fixtures = ['claraweb/backend/tests/fixtures/Services.yaml']
    initial_data = {'name': 'abcdefghijklmnopqrs'}
    initial_data_complete = {'dpe': 1, 'name': 'somelongname.'}

    def test_create_node_container(self):
        '''
        We must ensure that the container instance gets created
        correctly into the database

        Parameters
        ==========
        URL:/dpes/2/containers/
        data: {name:abc}
        method: POST
        Should Return HTTP_201_CREATED
        '''
        response = self.client.post('/dpes/1/containers/', self.initial_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_node_container_twice(self):
        '''
        We must ensure that the container instance gets created
        correctly into the database

        Parameters
        ==========
        URL:/dpes/2/containers/
        data: {name:abc}
        method: POST
        Should Return HTTP_201_CREATED
        '''
        self.client.post('/dpes/1/containers/', self.initial_data, format='json')
        response = self.client.post('/dpes/1/containers/', self.initial_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_node_container_bad(self):
        '''
        We must ensure that the container instance rejects the creation
        with the proper exception (bad dpe id)

        Parameters
        ==========
        URL:/dpes/200/containers/
        data: {name:abc}
        method: POST
        Should Return HTTP_400_BAD_REQUEST
        '''
        response = self.client.post('/dpes/200/containers/', self.initial_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_node_container(self):
        '''
        We must ensure that the container instance gets deleted
        correctly into the database under delete request

        Parameters
        ==========
        URL:/dpes/2/containers/2
        data: {name:abc}
        method: DELETE
        Should Return HTTP_204_NO_CONTENT
        '''
        response = self.client.delete('/dpes/2/containers/2', format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_delete_node_container_bad(self):
        '''
        We must ensure that the container instance gets the right exception
        when deleted with bad container id

        Parameters
        ==========
        URL:/dpes/2/containers/1000
        data: {name:abc}
        method: DELETE
        Should Return HTTP_404_NOT_FOUND
        '''
        response = self.client.delete('/dpes/2/containers/2000', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_container_request_obtains_filtered_data(self):
        response = self.client.get('/containers/?filter_by_containername=abc')
        self.assertEqual(2, len(response.data))
        response = self.client.get('/containers/?filter_by_servicename=calibration')
        self.assertEqual(2, len(response.data))

    def test_filter_container_request_obtains_filtered_data_for_specific_dpe(self):
        response = self.client.get('/dpes/3/containers/?filter_by_containername=abc')
        self.assertEqual(1, len(response.data))
        response = self.client.get('/dpes/3/containers/?filter_by_servicename=calibration')
        self.assertEqual(1, len(response.data))
        response = self.client.get('/dpes/2/containers/?filter_by_servicename=calibration')
        self.assertEqual(1, len(response.data))
        response = self.client.get('/dpes/3/containers/?filter_by_servicename=super')
        self.assertEqual(1, len(response.data))