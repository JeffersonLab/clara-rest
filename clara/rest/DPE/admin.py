# coding=utf-8

from clara.DPE.models import Node
from clara.Service.models import ServiceEngine
from django.contrib.admin import ModelAdmin, TabularInline, site

from clara.rest.Container import Container


class ContainerInline(TabularInline):
    model = Container
    fields = ('name',)


class NodeAdmin(ModelAdmin):
    model = Node
    readonly_fields = ('modified',)
    inlines = (ContainerInline, )


class ServiceEngineAdmin(ModelAdmin):
    model = ServiceEngine
    readonly_fields = ('modified',)


class ContainerAdmin(ModelAdmin):
    model = Container
    readonly_fields = ('modified',)

site.register(Node, NodeAdmin)
site.register(Container, ContainerAdmin)
site.register(ServiceEngine, ServiceEngineAdmin)

