'''
Created on 06-03-2015

@author: royarzun
'''
from django.http import HttpResponse
import json
'''
Nodes Views:
Views for json responses for the Clara Nodes (DPE) components
'''

def index(request):
    #show all of DPE Nodes
    response_data = {}
    return HttpResponse(json.dumps(response_data))

def update(request):
    #update one of the nodes (adding services or xmsg objects)
    response_data = {}
    return HttpResponse(json.dumps(response_data))

def destroy(request):
    #destroys a DPE a specific node
    response_data = {}
    return HttpResponse(json.dumps(response_data))