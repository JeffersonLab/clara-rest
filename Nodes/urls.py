'''
Created on 10-03-2015

@author: royarzun
'''
from django.conf.urls import patterns, url, include
from Nodes.views import index


urlpatterns = patterns('',
    url(r'^$', index),
    #url(r'^(?P<nodeid>[\w|-]{36})/$', show),



)
