'''
Created on 06-03-2015

@author: royarzun
'''
from django.conf.urls import patterns, url
from FrontEnd.views import *


urlpatterns = patterns('',
    url(r'^$', index),
    url(r'(?P<feid>\d+)/$', show)
)
