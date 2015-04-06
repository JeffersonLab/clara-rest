'''
Created on 06-04-2015

@author: royarzun
'''
from django.conf.urls import patterns, url

from views import ServiceEngineNestedList, ServiceEngineNestedDetail

urlpatterns = patterns('',
                       url(r'^/?$',
                           ServiceEngineNestedList.as_view()),
                       url(r'^(?P<service_id>\d+)/?$',
                           ServiceEngineNestedDetail.as_view())
                       )
