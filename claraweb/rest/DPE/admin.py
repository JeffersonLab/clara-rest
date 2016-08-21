# coding=utf-8

from claraweb.rest.Container.models import Container
from claraweb.rest.DPE.models import DPE
from claraweb.rest.Service.models import ServiceEngine
from django.contrib.admin import ModelAdmin, TabularInline, site


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

