'''
Created on 06-03-2015

@author: royarzun
'''
from django.http import HttpResponse 
from django.core import serializers
from FrontEnd.models import FrontEnd
from Nodes.models import Node
import json
'''
Nodes Views:
Views for json responses for the Clara Nodes (DPE) components
'''

def index(request, feid):
    #show all of DPE Nodes
    data = serializers.serialize('json', Node.objects.filter(frontend__celery_id=feid), fields=('ip','celery_id'))
    data = json.dumps(json.loads(data), indent=4)
    return HttpResponse(data, content_type="application/json")

def update(request):
    #update one of the nodes (adding services or xmsg objects)
    response_data = {}
    return HttpResponse(json.dumps(response_data))

def destroy(request):
    #destroys a DPE a specific node
    response_data = {}
    return HttpResponse(json.dumps(response_data))