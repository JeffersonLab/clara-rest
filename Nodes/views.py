'''
Created on 06-03-2015

@author: royarzun
'''
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from serializers import NodeSerializer, NodeDeployerSerializer
from models import Node
"""
Nodes Views:
Views for json responses for the Clara Nodes (DPE) components
"""


class Dpes(APIView):

    def get(self, request, format=None):
        """
        Find DPEs that match the optional query parameters.
        For all DPEs omit the parameters.
        ---
        parameters:
            - name: DPE_regex
              type: string
              paramType: query
              description: Regular expression of DPE ID
            - name: container_regex
              type: string
              paramType: query
              description: Regular expression of container ID
            - name: service_regex
              type: string
              paramType: query
              description: Regular expression of service ID
        responseMessages:
            - code: 401
              message: Not authenticated
        """
        # Regex filters
        dpe_regex = request.GET.get('DPE_regex')
        container_regex = request.GET.get('container_regex')
        service_regex = request.GET.get('service_regex')
        print "dpe_regex : "+dpe_regex
        print "container_regex : "+container_regex
        print "service_regex : "+service_regex
        node_objects = Node.objects.all()
        serializer = NodeSerializer(node_objects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Start new DPE(s)
        ---
        parameters_strategy:
            form: replace
        parameters:
            - name: DPEInfo
              type: string
              description: Quantity and types of DPEs to start
        response_serializer: Nodes.serializers.NodeSerializer
        responseMessages:
            - code: 400
              message: Bad Request
            - code: 401
              message: Not authenticated
        """
        # TODO: Types of DPE?
        serializer = NodeDeployerSerializer(data=request.data)
        if serializer.is_valid():
            # TODO: Here we use the methods to deploy new(s) DPE Instances
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Dpe(APIView):

    def get_object(self, DPE_id):
        try:
            return Node.objects.get(node_id=DPE_id)
        except Node.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, DPE_id, format=None):
        """
        Retrieve, update or delete a DPE instance.
        ---
        parameters:
            - name: DPE_id
              description: ID of DPE
              required: True
              paramType: path
              type: string
        response_serializer: Nodes.serializers.NodeSerializer
        responseMessages:
            - code: 400
              message: Bad request
            - code: 401
              message: Not authenticated
            - code: 404
              message: Resource not found
        """
        try:
            node_object = self.get_object(DPE_id)
            serializer = NodeSerializer(node_object)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, DPE_id, format=None):
        """
        Shutdown a Dpe
        ---
        parameters:
            - name: DPE_id
              description: ID of DPE
              required: True
              paramType: path
              type: string
        responseMessages:
            - code: 400
              message: Bad request
            - code: 401
              message: Not authenticated
            - code: 404
              message: Resource not found
        """
        node_object = self.get_object(DPE_id)
        node_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
