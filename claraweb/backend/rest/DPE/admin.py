# coding=utf-8

from django.contrib.admin import ModelAdmin, TabularInline, site

from backend.rest.Container.models import Container
from backend.rest.DPE.models import DPE
from backend.rest.Service.models import ServiceEngine


class ContainerInline(TabularInline):
    model = Container
    fields = ('name',)


class NodeAdmin(ModelAdmin):
    model = DPE
    readonly_fields = ('modified',)
    inlines = (ContainerInline, )


class ServiceEngineAdmin(ModelAdmin):
    model = ServiceEngine
    readonly_fields = ('modified',)


class ContainerAdmin(ModelAdmin):
    model = Container
    readonly_fields = ('modified',)

site.register(DPE, NodeAdmin)
site.register(Container, ContainerAdmin)
site.register(ServiceEngine, ServiceEngineAdmin)

