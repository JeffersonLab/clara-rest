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


class ContainerTests(APITestCase):
    fixtures = ['tests/fixtures/Services.yaml']
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
        pass
#         response = self.client.post(self.url_nested,
#                                     self.initial_data,
#                                     format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertContains(response=response, text="abc", count=1,
#                             status_code=201, msg_prefix="", html=False)

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
        response = self.client.post(self.url_nested_bad, self.initial_data,
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
        pass
#         response = self.client.delete(self.url_del, format='json')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

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
        container_data = {'name': 'abcdefghijk', 'dpe': '2'}
        response = self.client.post(self.url_container, container_data,
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
        container_bad_data = {'name': 'abcdefghijk', 'dpe': '2000'}
        response = self.client.post(self.url_container, container_bad_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_container_bad(self):
        '''
        We must ensure that the container instance gets the right exception
        when deleted with a bad id

        Parameters
        ==========
        URL:/containers/2000
        method: DELETE
        Should Return HTTP_404_NOT_FOUND
        '''
        response = self.client.delete(self.url_container_bad, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_container_request_obtains_filtered_data(self):
        response = self.client.get(self.url_container + '?filter_by_containername=abc')
        self.assertEqual(2, len(response.data))
        response = self.client.get(self.url_container + '?filter_by_servicename=calibration')
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