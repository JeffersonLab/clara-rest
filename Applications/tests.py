'''
Created on 08-04-2015

@author: royarzun
'''
from rest_framework import status
from rest_framework.test import APITestCase
from Applications.serializers import AppSerializer

class AppTests(APITestCase):
    fixtures = ['fixtures/Applications.yaml', ]
    url = '/applications/'
    url_bad = '/applications/1000'
    query = 'something'
    app_id = '1'
    app_id_bad = '1000'
    initial_data = ''
    
    def test_get_applications_all(self):
        '''
        We must ensure that we get the App index correctly
        
        Parameters
        ==========
        URL:/applications/
        method: GET
        Should Return HTTP_200_OK
        '''
        print "\n- Testing get applications all"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_applications_query(self):
        '''
        We must ensure that we get the App index correctly, limiting the output by
        using query parameters
        
        Parameters
        ==========
        URL:/applications/query?
        method: GET
        Should Return HTTP_200_OK
        '''
        print "\n- Testing get applications by query"
        response = self.client.get(self.url+self.query)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_application(self, app_id=None):
        '''
        We must ensure we get the app by its app_id correctly
        
        Parameters
        ==========
        URL:/applications/
        method: GET
        Should Return HTTP_200_OK
        '''
        print "\n- Testing get applications by application_id"
        if app_id is None:
            url = self.url+self.app_id
        else:
            url = self.url+app_id
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_application_bad(self):
        '''
        We must ensure we get the correct exceptions with a bad app_id
        
        Parameters
        ==========
        URL:/applications/1000
        method: GET
        Should Return HTTP_404_NOT_FOUND
        '''
        print "\n- Testing get applications by application_id (bad)"
        response = self.client.get(self.url+self.app_id_bad)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_application(self):
        '''
        We must ensure we delete the app using a correct app_id to do so
        
        Parameters
        ==========
        URL:/applications/1
        method: DELETE
        Should Return HTTP_204_NO_CONTENT
        '''
        print "\n- Testing delete applications by application_id"
        response = self.client.delete(self.url+self.app_id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_application_bad(self):
        '''
        We must ensure we get the right exceptions when delete the app using a bad app_id
        
        Parameters
        ==========
        URL:/applications/1000
        method: DELETE
        Should Return HTTP_404_NOT_FOUND
        '''
        print "\n- Testing delete applications by application_id (bad)"
        response = self.client.delete(self.url+self.app_id_bad)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_create_and_run_app(self):
        '''
        Tests the creation in the DB of an application and
        makes sure it runs properly and registers its activity
        
        Parameters
        ==========
        URL:/applications/1000
        method: POST
        Should Return HTTP_201_CREATED
        '''
        print "\n- Testing app deployment in the cloud"
        
        data = {"registered_class": "SomeOtherClass.Other.More",
                "chain": {"services": "Service1, Service2, Service3"},
                "input": "","output": ""}
        
        
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
