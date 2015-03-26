'''
Created on 26-03-2015

@author: royarzun
'''
from django.conf.urls import patterns, url

from views import SubscriptionList, SubscriptionDetail

urlpatterns = patterns('',
                       url(r'^/?$', SubscriptionList.as_view()),
                       url(r'^(?P<subscription_id>[\d+])/?', SubscriptionDetail.as_view())
                       )
