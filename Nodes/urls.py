'''
Created on 10-03-2015

@author: royarzun
'''
from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url(r'^$', views.NodeList.as_view()),
    url(r'^(?P<nodeid>[\w|-]{36})$', views.NodeDetail.as_view())
)
