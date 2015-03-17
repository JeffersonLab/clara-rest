'''
Created on 06-03-2015

@author: royarzun
'''
from django.conf.urls import patterns, url, include
import views


urlpatterns = patterns('',
                       url(r'^\/?$', views.FrontEndList.as_view()),
                       url(r'^(?P<feid>[\w|-]{36}/?)$',
                           views.FrontEndDetail.as_view()),
                       url(r'^(?P<feid>[\w|-]{36})/nodes/',
                           include('Nodes.urls'))
                       )
