#!/usr/bin/env python
#
# Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its
# documentation for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement.
#
# Author Ricardo Oyarzun
# Department of Experimental Nuclear Physics, Jefferson Lab.
#
# IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
# INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
# THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
#
# JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
# HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
# SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#

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
        response = self.client.get(self.url_get)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response=response,
                            text="\"engine_class\":\"superReconstructorService\"", 
                            count=1, status_code=200, msg_prefix="", html=False)
        
    def test_delete_service_engine(self):
        pass
