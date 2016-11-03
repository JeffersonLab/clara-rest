# coding=utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = patterns('',
                       url(r'^/?$', RedirectView.as_view(url='/dpes',
                                                         permanent=True,
                                                         query_string=False)),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api-auth/',
                           include('rest_framework.urls',
                                   namespace='rest_framework')),
                       url(r'^docs/', schema_view),
                       url(r'^dpes/',
                           include('claraweb.backend.rest.DPE.urls')),
                       url(r'^containers/',
                           include('claraweb.backend.rest.Container.urls')),
                       url(r'^services/',
                           include('claraweb.backend.rest.Service.urls')),
                       )

urlpatterns = format_suffix_patterns(urlpatterns)
