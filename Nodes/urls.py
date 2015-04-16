'''
Created on 10-03-2015

@author: royarzun
'''
from django.conf.urls import patterns, url

from views import Dpe, Dpes

urlpatterns = patterns('',
                       url(r'^$', Dpes.as_view()),
                       url(r'^(?P<DPE_id>[\d+])/?$', Dpe.as_view()),
                       )
