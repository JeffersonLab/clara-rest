#
# Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its
# documentation for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement.
#
# Author Ricardo Oyarzun
# Department of Experimental Nuclear Physics, Jefferson Lab.
#
# IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
# INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
# THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
#
# JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
# HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
# SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#

from django.contrib.admin import ModelAdmin, TabularInline, site

from Applications.models import App, Chain
from Nodes.models import Node
from Nodes.Container.models import Container
from Nodes.Container.Service.models import ServiceEngine


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
