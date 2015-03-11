'''
Created on 06-03-2015

@author: royarzun
'''
from django.conf.urls import patterns, url, include
import views


urlpatterns = patterns('',
    url(r'^frontends/$', views.fe_list),
    url(r'^frontends/(?P<feid>[\w|-]{36})/$', views.fe_detail),
    url(r'^frontends/(?P<feid>[\w|-]{36})/nodes', include('Nodes.urls'))
)
