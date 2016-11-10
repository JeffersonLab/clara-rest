# coding=utf-8

from django.conf.urls import patterns, include, url
from views import ContainersView, ContainerView
from claraweb.backend.rest.url_re_patterns import URLPattern

urlpatterns = patterns('',
                       url(r'^$', ContainersView.as_view(), name='container-list'),
                       url(URLPattern.CONTAINER_URL + '/?$',
                           ContainerView.as_view(), name='container-detail'),
                       url(URLPattern.CONTAINER_URL + '/services/',
                           include('claraweb.backend.rest.Service.urls'))
                       )
