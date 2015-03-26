'''

Created on 06-03-2015
@author: royarzun
'''
from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic.base import RedirectView


urlpatterns = patterns('',
                       url(r'^/?$', RedirectView.as_view(url='/dpes', permanent=True, query_string=False)),  
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api-auth/', include('rest_framework.urls',
                                                  namespace='rest_framework')
                           ),
                       url(r'^dpes/', include('Nodes.urls')),
                       url(r'^subscriptions/', include('Subscription.urls'))
                       )

urlpatterns = format_suffix_patterns(urlpatterns)
