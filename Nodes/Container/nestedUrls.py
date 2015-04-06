'''
Created on 01-04-2015

@author: royarzun
'''
from django.conf.urls import patterns, url, include

from views import ContainerNestedList, ContainerNestedDetail

urlpatterns = patterns('',
                       url(r'^(?P<DPE_id>\d+)/containers/?$',
                           ContainerNestedList.as_view()),
                       url(r'^(?P<DPE_id>\d+)/containers/(?P<container_id>\d+)/?$',
                           ContainerNestedDetail.as_view()),
                       url(r'^(?P<DPE_id>\d+)/containers/(?P<container_id>\d+)/services/',
                           include('Nodes.Container.Service.nestedUrls'))
                       )
