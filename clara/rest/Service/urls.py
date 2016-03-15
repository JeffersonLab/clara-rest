# coding=utf-8

from django.conf.urls import patterns, url

from clara.rest.Service.views import ServicesView, ServiceView

urlpatterns = patterns('',
                       url(r'^$',ServicesView.as_view(), name='service-list'),
                       url(r'^(?P<service_id>[a-z0-9]+)/?$', ServiceView.as_view(),
                           name='service-detail'),
                       )
