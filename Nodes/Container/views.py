'''
Created on 24-03-2015

@author: royarzun
'''
from django.http import Http404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from serializers import ContainerSerializer
from Nodes.models import Node
from models import Container
'''
Container views:
Views for json responses for the Clara Containers at Specific Hostname (DPE)
'''


class ContainerList(APIView):
    """
    List of all Containers at specific DPE
    """
    def get(self, request,nodeid, format=None):
        container_objects = Node.objects.get(node_id=nodeid).containers.all()
        serializer = ContainerSerializer(container_objects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ContainerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContainerDetail(APIView):
    """
    Retrieve, update or delete a Container instance.
    """
    def get_object(self, containerid):
        try:
            return Container.objects.get(name=containerid)
        except Container.DoesNotExist:
            raise Http404

    def get(self, request, nodeid, containerid, format=None):
        container_object = self.get_object(containerid)
        serializer = ContainerSerializer(container_object)
        return Response(serializer.data)

    def put(self, request, containerid, format=None):
        container_object = self.get_object(containerid)
        serializer = ContainerSerializer(container_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, containerid, format=None):
        container_object = self.get_object(containerid)
        container_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
