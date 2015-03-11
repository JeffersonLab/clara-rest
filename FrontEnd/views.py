#from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from FrontEnd.models import FrontEnd

from celery.task.control import revoke
from tasks import start_fe_task, get_task_status
import json

'''
FrontEnd Views:
Views for json responses for the Clara Frontend (PLATFORM) components
'''

def index(request):
    data = serializers.serialize('json', FrontEnd.objects.filter(status='Active'), fields=('hostname','celery_id'))
    data = json.dumps(json.loads(data), indent=4)
    return HttpResponse(data, content_type="application/json")    

def show(request, feid,):
    data = get_task_status(feid)
    data = json.dumps(json.loads(data), indent=4)
    return HttpResponse(data, content_type="application/json")

def create(request):
    pid = start_fe_task.delay('Hello World!')
    fe_object = FrontEnd()
    fe_object.celery_id = pid
    fe_object.ip = '127.0.0.1'
    fe_object.status ='Active'
    fe_object.save()
    data = get_task_status(pid.id)
    return HttpResponse(data, content_type="application/json")

def destroy(request, feid):
    fe_object = FrontEnd.objects.get(celery_id=feid)
    fe_object.status = 'Stopped'
    fe_object.save()
    revoke(feid, terminate=True)
    return HttpResponse(json.dumps({'id' : feid, 'status' : 'DESTROYED'}))