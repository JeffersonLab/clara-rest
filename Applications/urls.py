'''
Created on 09-04-2015

@author: royarzun
'''
from django.conf.urls import patterns, url

from views import AppList, AppDetail

urlpatterns = patterns('',
                       url(r'^/?$', AppList.as_view()),
                       url(r'^(?P<application_id>[\d+])/?$', AppDetail.as_view())
                       )
