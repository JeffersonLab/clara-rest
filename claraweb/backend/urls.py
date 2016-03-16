# coding=utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns('',
                       url(r'^/?$', RedirectView.as_view(url='/dpes',
                                                         permanent=True,
                                                         query_string=False)),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api-auth/',
                           include('rest_framework.urls',
                                   namespace='rest_framework')),
                       url(r'^docs/',
                           include('rest_framework_swagger.urls')),
                       url(r'^dpes/',
                           include('claraweb.rest.DPE.urls')),
                       url(r'^containers/',
                           include('claraweb.rest.Container.urls')),
                       url(r'^services/',
                           include('claraweb.rest.Service.urls')),
                       )

urlpatterns = format_suffix_patterns(urlpatterns)
