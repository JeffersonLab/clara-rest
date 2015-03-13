'''
Created on 06-03-2015

@author: royarzun
'''
from django.http import HttpResponse 
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from serializers import NodeSerializer
from models import Node
'''
Nodes Views:
Views for json responses for the Clara Nodes (DPE) components
'''
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@api_view(['GET', 'POST'])
def node_list(request):
    """
    List all nodes, or create a new one.
    """
    if request.method == 'GET':
        node_objects = Node.objects.all()
        serializer = NodeSerializer(node_objects, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = NodeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def node_detail(request, nodeid):
    """
    Retrieve, update or delete a node
    """
    try:
        node_object = Node.objects.get(celery_id=nodeid)
    except Node.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = NodeSerializer(node_object)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = NodeSerializer(node_object, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        node_object.delete()
        return HttpResponse(status=204)