from django.conf.urls import patterns, include, url
from django.contrib import admin
'''
Created on 06-03-2015

@author: royarzun
'''

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^FrontEnd/', include('FrontEnd.urls'))
)
