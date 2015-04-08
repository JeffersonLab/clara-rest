'''
Created on 27-03-2015

@author: royarzun
'''
from rest_framework import status
from rest_framework.test import APITestCase


class ContainerTests(APITestCase):
    fixtures = ['fixtures/Nodes.yaml', 'fixtures/Container.yaml']
    url_nested = '/dpes/2/containers/'
    url_nested_bad = '/dpes/200/containers/'
    url_container = '/containers/'
    url_del = url_nested+'1'
    url_del_bad = url_nested+'1000'
    url_del_container = url_container+'1'
    url_container_bad = url_container+'2000'
    initial_data = {'name': 'abc'}

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
        print "\n- Testing Node/Container create method"
        response = self.client.post(self.url_nested,
                                    self.initial_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertContains(response=response, text="abc", count=1,
                            status_code=201, msg_prefix="", html=False)
        
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
        print "\n- Testing Node/Container create method (bad node_id)"
        response = self.client.post(self.url_nested_bad,
                                    self.initial_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_node_container(self):
        '''
        We must ensure that the container instance gets deleted
        correctly into the database under delete request
        
        Parameters
        ==========
        URL:/dpes/2/containers/1
        data: {name:abc}
        method: DELETE
        Should Return HTTP_204_NO_CONTENT
        '''
        print "\n- Testing Node/Container delete method"
        response = self.client.delete(self.url_del, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
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
        print "\n- Testing Node/Container delete method (bad container_id)"
        response = self.client.delete(self.url_del_bad, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_container(self):
        '''
        We must ensure that the container instance gets created
        correctly into the database
        
        Parameters
        ==========
        URL:/containers/
        data: {name: abcdefghijk, dpe: 2}
        method: POST
        Should Return HTTP_201_CREATED
        '''
        print "\n- Testing Container create method"
        container_data = {'name': 'abcdefghijk', 'dpe': '2'}
        response = self.client.post(self.url_container,
                                    container_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_container_bad(self):
        '''
        We must ensure that the container instance gets created
        correctly into the database
        
        Parameters
        ==========
        URL:/containers/
        data: {name: abcdefghijk, dpe: 2000}
        method: POST
        Should Return HTTP_400_BAD_REQUEST
        '''
        print "\n- Testing Container create method (bad data)"
        container_bad_data = {'name': 'abcdefghijk', 'dpe': '2000'}
        response = self.client.post(self.url_container,
                                    container_bad_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

    def test_delete_container(self):
        '''
        We must ensure that the container instance gets deleted
        correctly into the database under delete request
        
        Parameters
        ==========
        URL:/containers/1
        method: DELETE
        Should Return HTTP_204_NO_CONTENT
        '''
        print "\n- Testing Container delete method"
        response = self.client.delete(self.url_del_container, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_delete_container_bad(self):
        '''
        We must ensure that the container instance gets the right exception when deleted
        with a bad id
        
        Parameters
        ==========
        URL:/containers/2000
        method: DELETE
        Should Return HTTP_404_NOT_FOUND
        '''
        print "\n- Testing Container delete method (bad container_id)"
        response = self.client.delete(self.url_container_bad, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)