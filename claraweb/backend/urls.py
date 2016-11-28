# coding=utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^docs/', include('rest_framework_swagger.urls')),
                       url(r'^dpes/',
                           include('backend.rest.DPE.urls')),
                       url(r'^containers/',
                           include('backend.rest.Container.urls')),
                       url(r'^services/',
                           include('backend.rest.Service.urls')),
                       )

urlpatterns = format_suffix_patterns(urlpatterns)
