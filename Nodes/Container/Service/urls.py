'''
Created on 31-03-2015

@author: royarzun
'''
from django.conf.urls import patterns, url

from views import ServiceEngineList

urlpatterns = patterns('', url(r'^$', ServiceEngineList.as_view()))
