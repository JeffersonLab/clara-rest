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
    def test_deploy_service(self):
        """
        We must safely deploy a service into a container
        from the API
        """
        print "\n- Deploying a service into existent container"
        response = self.client.post(self.url_create,
                                    self.initial_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # if passes, service was deployed
    
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
