# coding=utf-8

from django.conf.urls import patterns, url
from claraweb.rest.url_re_patterns import URLPattern
from claraweb.rest.Service.views import ServicesView, ServiceView

urlpatterns = patterns('',
                       url(r'^$',ServicesView.as_view(),
                           name='service-list'),
                       url(URLPattern.SERVICE_URL, ServiceView.as_view(),
                           name='service-detail'),
                       )
