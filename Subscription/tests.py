'''
Created on 26-03-2015

@author: royarzun
'''
import json
from rest_framework import status
from rest_framework.test import APITestCase


class SubscriptionTests(APITestCase):
    fixtures = ['fixtures/Subscription.yaml', ]
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
        print "\n- Testing Subscription create method"
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
        print "\n- Testing Subscription create method"
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
        print "\n- Testing Subscription delete method"
        response = self.client.delete(self.url_del, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
