'''
Created on 06-03-2015

@author: royarzun
'''
from django.http import Http404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from serializers import NodeSerializer
from models import Node
'''
Nodes Views:
Views for json responses for the Clara Nodes (DPE) components
'''


class NodeList(APIView):
    """
    Find DPEs that match the optional query parameters. For all DPEs omit the parameters.
    """
    def get(self, request, format=None):
        node_objects = Node.objects.all()
        serializer = NodeSerializer(node_objects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NodeDetail(APIView):
    """
    Retrieve, update or delete a DPE instance.
    """
    def get_object(self, DPE_id):
        try:
            return Node.objects.get(node_id=DPE_id)
        except Node.DoesNotExist:
            raise Http404

    def get(self, request, DPE_id, format=None):
        node_object = self.get_object(DPE_id)
        serializer = NodeSerializer(node_object)
        return Response(serializer.data)

    def put(self, request, DPE_id, format=None):
        node_object = self.get_object(DPE_id)
        serializer = NodeSerializer(node_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, DPE_id, format=None):
        node_object = self.get_object(DPE_id)
        node_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
