# coding=utf-8

from django.conf.urls import patterns, include, url
from backend.rest.url_re_patterns import URLPattern
from backend.rest.DPE.views import Dpe, Dpes

urlpatterns = patterns('',
                       url(r'^$', Dpes.as_view(),
                           name="dpe-list"),
                       url(URLPattern.DPE_URL + '/?$', Dpe.as_view(),
                           name="dpe-detail"),
                       url(URLPattern.DPE_URL + '/containers/',
                           include('backend.rest.Container.urls')),
                       )
