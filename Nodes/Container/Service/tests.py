'''
Created on 06-04-2015

@author: royarzun
'''
from rest_framework import status
from rest_framework.test import APITestCase


class ServiceEngineTests(APITestCase):
    fixtures = ['fixtures/Services.yaml',]
    url_create = '/dpes/1/containers/1/services/'
    url_get = '/dpes/1/containers/1/services/1'
    initial_data = {
                    "engine_class": "some_class",
                    "threads": 1,
                    "configuration": "some_config"
                    }
    bad_data = {
                "threads": 1,
                "configuration": "some_config"
                }
    
    def test_deploy_service(self):
        """
        We must safely deploy a service into a container
        from the API
        
        Parameters
        ==========
        URL:/dpes/1/containers/1/service
        data: {engine_class:some_class,threads:1,configuration:some_config}
        method: POST
        Should Return HTTP_201_CREATED
        """
        print "\n- Deploying a service into existent container"
        response = self.client.post(self.url_create,
                                    self.initial_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_deploy_service_bad(self):
        """
        We must ensure bad data gets proper exception and response
        
        Parameters
        ==========
        URL:/dpes/100/containers/1/service
        data: {engine_class:some_class,threads:1,configuration:some_config}
        method: POST
        Should Return HTTP_201_CREATED
        """
        print "\n- Deploying a service into existent container"
        response = self.client.post('/dpes/100/containers/1/services/',
                                    self.initial_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post('/dpes/1/containers/100/services/',
                                    self.initial_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    
    def test_get_service_engine(self):
        """
        From the created service, we need to retrieve its registration
        information 
        """
        print "\n- Getting the registration information from the deployed service"
        response = self.client.get(self.url_get)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response=response,
                            text="\"engine_class\":\"superReconstructorService\"", 
                            count=1, status_code=200, msg_prefix="", html=False)
        
    def test_delete_service_engine(self):
        pass
