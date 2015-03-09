#from django.shortcuts import render
from django.http import HttpResponse
import json
import tasks
'''
FrontEnd Views:
Views for json responses for the Clara Frontend (PLATFORM) components
'''

def index(request):
    response_data = {}
    return HttpResponse(json.dumps(response_data))

def show(request, feid):
    response_data = tasks.get_task_status(feid)
    return HttpResponse(json.dumps(response_data))

def create(request):
    pid = tasks.StartNodeDPETask.delay("Hola")
    return HttpResponse(json.dumps(tasks.get_task_status(pid.id)))