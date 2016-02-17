#!/usr/bin/env python
#
# Copyright (C) 2015. Jefferson Lab, Clara framework (JLAB). All Rights Reserved.
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

from django.test import TransactionTestCase
from rest_framework import status
from rest_framework.test import APITestCase


class ServiceEngineDBTransactionTest(TransactionTestCase):

    def test_create_transaction_without_override(self):
        pass


class ServiceEngineTests(APITestCase):
    fixtures = ['ClaraWebREST/tests/fixtures/Services.yaml',]
    initial_data = {
                    "engine_name": "some_engine_to_try_install",
                    "class_name": "some_class",
                    "author": "Jarvis",
                    "version": "1.0",
                    "description": "algo"
                    }
    initial_data_complete_bad = {
                                "container": 100000,
                                "engine_name": "some_engine_to_try_install-2",
                                "class_name": "some_class",
                                "author": "Jarvis",
                                "version": "2.0",
                                "description": "algo"
                                }
    initial_data_complete = {
                            "container": 3,
                            "engine_name": "some_engine_to_try_install-3",
                            "class_name": "some_class",
                            "author": "Jarvis",
                            "version": "3.0",
                            "description": "algo"
                            }

    bad_data = {}

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
        response = self.client.post('/dpes/1/containers/1/services/',
                                    self.initial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_deploy_service_not_nested_url(self):
        """
        Service should deploy with a full set of data

        Parameters
        ==========
        URL:/service/
        data: self.initial_data_complete
        method: POST
        Should Return HTTP_201_CREATED
        """
        response = self.client.post('/services/',self.initial_data_complete, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_deploy_service_not_nested_url_twice(self):
        """
        Service should deploy with a full set of data

        Parameters
        ==========
        URL:/service/
        data: self.initial_data_complete
        method: POST
        Should Return HTTP_201_CREATED
        """
        self.client.post('/services/',self.initial_data_complete, format='json')
        response = self.client.post('/services/',self.initial_data_complete, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deploy_service_not_nested_url_bad(self):
        """
        Service should not be deployed with bad data

        Parameters
        ==========
        URL:/service/
        data: self.initial_data_complete_bad
        method: POST
        Should Return HTTP_400_BAD_REQUEST
        """
        response = self.client.post('/services/',self.initial_data_complete_bad, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deploy_service_twice_does_not_overwrite(self):
        """
        We must safely deploy a service into a container twice does not
        overwrite the previous database instance

        Parameters
        ==========
        URL:/dpes/1/containers/1/service
        data: {engine_class:some_class,threads:1,configuration:some_config}
        method: POST
        Should Return HTTP_201_CREATED
        """
        # response = self.client.post('/dpes/1/containers/1/services/',
        #                             self.initial_data,
        #                             format='json')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # response = self.client.post('/dpes/1/containers/1/services/',
        #                             self.initial_data,
        #                             format='json')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)


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
        response = self.client.get('/dpes/1/containers/1/services/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response=response,
                            text="\"engine_name\":\"superReconstructorService\"",
                            count=1, status_code=200, msg_prefix="", html=False)

    def test_filter_service_request_obtains_filtered_data(self):
        response = self.client.get('/services/?filter_by_servicename=calibration')
        self.assertEqual(2, len(response.data))
        response = self.client.get('/services/?filter_by_description=BUGGGGGSS')
        self.assertEqual(2, len(response.data))
        # response = self.client.get('/services/?filter_by_language=java')
        # self.assertEqual(4, len(response.data))
        # response = self.client.get('/services/?filter_by_language=python')
        # self.assertEqual(1, len(response.data))
        response = self.client.get('/services/?filter_by_author=Jarvis')
        self.assertEqual(4, len(response.data))
        response = self.client.get('/services/?filter_by_author=Vardan')
        self.assertEqual(1, len(response.data))

    def test_filter_service_request_obtains_filtered_data_for_specific_container(self):
        response = self.client.get('/dpes/1/containers/1/services/?filter_by_name=BUGGGGGSS')
        self.assertEqual(1, len(response.data))
        response = self.client.get('/dpes/3/containers/3/services/?filter_by_description=BUGGGGGSS')
        self.assertEqual(1, len(response.data))
        response = self.client.get('/dpes/3/containers/3/services/?filter_by_description=algo')
        self.assertEqual(1, len(response.data))
        # response = self.client.get('/dpes/3/containers/3/services/?filter_by_language=java')
        # self.assertEqual(1, len(response.data))
        # response = self.client.get('/dpes/3/containers/3/services/?filter_by_language=python')
        # self.assertEqual(1, len(response.data))
        response = self.client.get('/dpes/3/containers/3/services/?filter_by_author=Jarvis')
        self.assertEqual(2, len(response.data))
