'''
Created on 31-03-2015

@author: royarzun
'''
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from serializers import ServiceEngineInfoSerializer
from models import ServiceEngineInfo
"""
Services Views:
Views for json responses for the Clara ServiceEngines
"""


class ServiceEngineList(APIView):

    def get(self, request, format=None):
        """
        Find services that match the optional query parameters.<br>
        For all services omit the parameters.
        ---
        parameters:
            - name: DPE_regex
              type: string            
              paramType: query
              description: Regular expression of the DPE id
              required: False
            - name: container_regex
              type: string
              paramType: query
              description: Regular expression of container id
              required: False
            - name: service_regex
              type: string
              paramType: query
              description: Regular expression for the Service Engine name
              required: False
        response_serializer: Nodes.Container.Service.serializers.ServiceEngineInfoSerializer
        """
        service_objects = ServiceEngineInfo.objects.all()
        serializer = ServiceEngineInfoSerializer(service_objects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Create a new service in one container at one DPE. The named container will be created if necessary.
        ---
        parameters:
            - name: container_id
              description: Container Id for the Service Engine
              required: True
            - name: engine_class
              description: Class name of the Service Engine
              required: True
            - name: configuration
              description: Service Configuration
              required: False
            - name: threads
              description: Number of threads for the Service Engine
              type: integer
              required: True
        request_serializer: Nodes.Container.Service.serializers.ServiceEngineInfoSerializer
        response_serializer: Nodes.Container.Service.serializers.ServiceEngineInfoSerializer
        """
        serializer = ServiceEngineInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
