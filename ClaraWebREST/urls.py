'''

Created on 06-03-2015
@author: royarzun
'''
from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api-auth/', include('rest_framework.urls',
                                                  namespace='rest_framework')
                           ),
                       url(r'^DPE/', include('Nodes.urls'))
                       )

urlpatterns = format_suffix_patterns(urlpatterns)
