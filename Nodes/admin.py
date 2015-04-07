'''
Created on 24-03-2015

@author: royarzun
'''
from django.contrib.admin import ModelAdmin, TabularInline, site

from Nodes.models import Node
from Container.models import Container
from Container.Service.models import ServiceEngine


class ContainerInline(TabularInline):
    model = Container
    fields = ('name',)


class NodeAdmin(ModelAdmin):
    model = Node
    readonly_fields = ('created', 'modified')
    inlines = (ContainerInline, )

class ServiceEngineAdmin(ModelAdmin):
    model = ServiceEngine
    readonly_fields = ('created', 'modified')
    
site.register(Node, NodeAdmin)
site.register(Container)
site.register(ServiceEngine, ServiceEngineAdmin)
