'''
Created on 10-03-2015

@author: royarzun
'''
from django.conf.urls import patterns, url
from views import NodeDetail, NodeList


urlpatterns = patterns('',
                       url(r'^$', NodeList.as_view()),
                       url(r'^(?P<nodeid>[\w|-]{36})$', NodeDetail.as_view())
                       )
