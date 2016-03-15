# coding=utf-8

from django.conf.urls import patterns, include, url

from clara.rest.DPE import Dpe, Dpes

urlpatterns = patterns('',
                       url(r'^$', Dpes.as_view(), name="node-list"),
                       url(r'^(?P<DPE_id>[a-z0-9]+)/?$', Dpe.as_view(),
                           name="node-detail"),
                       url(r'^(?P<DPE_id>[a-z0-9]+)/containers/',
                           include('clara.rest.Container.urls')),
                       )
