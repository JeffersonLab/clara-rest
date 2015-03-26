'''
Created on 26-03-2015
 
@author: royarzun
'''
from rest_framework import status
from rest_framework.test import APITestCase
 
 
class SubscriptionTests(APITestCase):
    fixtures = ['fixtures/Subscription.yaml',]
    url = '/subscriptions/'
    url_put = url+'1'
    url_del = url+'2'
    initial_data = {'type':'ERROR', 'sender':'CLOUD'}
     
    def test_create_sub(self):
        '''
        We must ensure that the Subscription instance gets created
        correctly into the database
        '''
        response = self.client.post(self.url, self.initial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
         
    def test_update_sub(self):
        '''
        We must ensure that the Subscription instance gets updated
        correctly into the database
        '''
        updated_data = {"type" : "ERROR", "sender" : "CLOUD"}
        response = self.client.put(self.url_put, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
         
     
    def test_delete_sub(self):
        '''    
        We must ensure that the Subscription instance gets deleted
        correctly into the database under delete request
        '''
        response = self.client.delete(self.url_del, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
