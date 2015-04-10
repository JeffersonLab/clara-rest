'''
Created on 24-03-2015

@author: royarzun
'''
from django.contrib.admin import ModelAdmin, TabularInline, site

from Nodes.models import Node
from Applications.models import App, Chain
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

    
class ContainerAdmin(ModelAdmin):
    model = Container
    readonly_fields = ('created', 'modified')


class ChainInline(TabularInline):
    model = Chain
    readonly_fields = ('app', )
    
class AppAdmin(ModelAdmin):
    model = App
    readonly_fields = ('created', 'modified')
    inlines = (ChainInline, )
    
site.register(Node, NodeAdmin)
site.register(Container, ContainerAdmin)
site.register(ServiceEngine, ServiceEngineAdmin)
site.register(App, AppAdmin)
