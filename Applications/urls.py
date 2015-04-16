'''
Created on 09-04-2015

@author: royarzun
'''
from django.conf.urls import patterns, url

from views import ClaraApps, ClaraApp

urlpatterns = patterns('',
                       url(r'^/?$', ClaraApps.as_view()),
                       url(r'^(?P<application_id>[\d+])/?$', ClaraApp.as_view())
                       )
