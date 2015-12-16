'''
Created on 25-03-2015

@author: royarzun
'''
from django.conf.urls import patterns, url

from views import ContainerList, ContainerDetail

urlpatterns = patterns('',
                       url(r'^$', ContainerList.as_view()),
                       url(r'^(?P<container_id>[a-z0-9]+)/?$',
                           ContainerDetail.as_view())
                       )
