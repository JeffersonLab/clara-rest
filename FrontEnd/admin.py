from django.contrib import admin

from Nodes.models import Node
from models import FrontEnd

class NodeInline(admin.TabularInline):
    model  = Node
    fields = ('hostname','status')


class FrontEndAdmin(admin.ModelAdmin):
    model = FrontEnd
    readonly_fields = ('created', 'modified', )
    inlines = (NodeInline, )
    
admin.site.register(FrontEnd, FrontEndAdmin)
