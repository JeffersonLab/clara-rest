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

import json
from rest_framework import status
from rest_framework.test import APITestCase


class SubscriptionTests(APITestCase):
    fixtures = ['tests/fixtures/Subscription.yaml', ]
    url = '/subscriptions/'
    url_get = url+'1'
    url_del = url+'2'
    initial_data = {'type': 'ERROR', 'sender': 'CLOUD'}

    def test_create_sub(self):
        '''
        We must ensure that the Subscription instance gets created
        correctly into the database
        
        Parameters
        ==========
        URL:/subscriptions/
        data: {type:ERROR,sender:CLOUD}
        method: POST
        Should Return HTTP_201_CREATED
        '''
        response = self.client.post(self.url, self.initial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_sub(self):
        '''
        We must ensure that the Subscription instance gets created
        correctly into the database
        
        Parameters
        ==========
        URL:/subscriptions/
        data: {type:ERROR,sender:CLOUD}
        method: POST
        Should Return HTTP_201_CREATED
        '''
        response = self.client.get(self.url_get)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_sub(self):
        '''
        We must ensure that the Subscription instance gets deleted
        correctly into the database under delete request
        
        Parameters
        ==========
        URL:/subscriptions/
        method: DELETE
        Should Return HTTP_204_NO_CONTENT
        '''
        response = self.client.delete(self.url_del, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
