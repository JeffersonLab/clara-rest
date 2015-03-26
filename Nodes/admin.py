'''
Created on 24-03-2015

@author: royarzun
'''
from django.contrib.admin import ModelAdmin, TabularInline, site

from Nodes.models import Node
from Container.models import Container


class ContainerInline(TabularInline):
    model  = Container
    fields = ('name',)


class NodeAdmin(ModelAdmin):
    model = Node
    readonly_fields = ('created','modified')
    inlines = (ContainerInline, )

    
site.register(Node, NodeAdmin)
site.register(Container)