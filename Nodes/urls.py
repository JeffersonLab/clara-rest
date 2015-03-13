'''
Created on 10-03-2015

@author: royarzun
'''
from django.conf.urls import patterns, url
from views import node_list, node_detail


urlpatterns = patterns('',
    url(r'^$', node_list),
    url(r'^(?P<nodeid>[\w|-]{36})/$', node_detail)
)
