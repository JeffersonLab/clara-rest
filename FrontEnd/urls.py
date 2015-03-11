'''
Created on 06-03-2015

@author: royarzun
'''
from django.conf.urls import patterns, url, include
from FrontEnd.views import show, create, index, destroy


urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^(?P<feid>[\w|-]{36})/$', show),
    url(r'^(?P<feid>[\w|-]{36})/nodes/', include('Nodes.urls')),
    url(r'^destroy/(?P<feid>[\w|-]{36})/$', destroy),
    url(r'^new$', create),
)
