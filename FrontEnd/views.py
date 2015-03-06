#from django.shortcuts import render
from django.http import HttpResponse
import json
'''
FrontEnd Views:
Views for json responses for the Clara Frontend (PLATFORM) components
'''

def index(request):
    response_data = {}
    print "Estoy en index: "
    return HttpResponse(json.dumps(response_data))

def show(request, feid):
    response_data = {
                     "id" : str(feid)
                     }
    print "Estoy en show: "
    
    return HttpResponse(json.dumps(response_data))