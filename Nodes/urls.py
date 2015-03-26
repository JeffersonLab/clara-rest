'''
Created on 10-03-2015

@author: royarzun
'''
from django.conf.urls import patterns, url, include

from views import NodeDetail, NodeList

urlpatterns = patterns('',
                       url(r'^$', NodeList.as_view()),
                       url(r'^(?P<nodeid>[\d+])/?$', NodeDetail.as_view()),
                       url(r'^(?P<nodeid>[\d+])/containers/', include('Nodes.Container.urls'))
                       )
