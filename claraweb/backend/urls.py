# coding=utf-8

from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Clara API')

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api-auth/',
                           include('rest_framework.urls',
                                   namespace='rest_framework')),
                       url(r'^docs/', schema_view),
                       url(r'^dpes/',
                           include('backend.rest.DPE.urls')),
                       url(r'^containers/',
                           include('backend.rest.Container.urls')),
                       url(r'^services/',
                           include('backend.rest.Service.urls')),
                       )

urlpatterns = format_suffix_patterns(urlpatterns)
