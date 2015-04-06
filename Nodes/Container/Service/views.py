'''
Created on 31-03-2015

@author: royarzun
'''
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from serializers import ServiceEngineSerializer, ServiceEngineNestedSerializer
from Nodes.models import Node
from Nodes.Container.models import Container
from models import ServiceEngine
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
        response_serializer: Nodes.Container.Service.serializers.ServiceEngineSerializer
        """
        service_objects = ServiceEngine.objects.all()
        serializer = ServiceEngineSerializer(service_objects, many=True)
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
        request_serializer: Nodes.Container.Service.serializers.ServiceEngineSerializer
        response_serializer: Nodes.Container.Service.serializers.ServiceEngineSerializer
        """
        serializer = ServiceEngineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceEngineNestedList(APIView):
    
    def get(self, request, DPE_id, container_id, format=None):
        """
        Get the registration information of the Service Engines for a specific container
        ---
        parameters:
            - name: DPE_id
              description: ID of DPE
              required: True
              paramType: path
              type: string
            - name: container_id
              description: ID of container
              required: True
              paramType: path
              type: string
        """
        service_objects = ServiceEngine.objects.all()
        serializer = ServiceEngineSerializer(service_objects, many=True)
        return Response(serializer.data)
    
    def post(self, request, DPE_id, container_id, format=None):
        """
        Deploy a new service at Container. The name of the container will be created if is not provided.
        ---
        parameters:
            - name: DPE_id
              description: Id of the DPE
              paramType: path
              type: string
              required: True
            - name: container_id
              description: Container Id for the Service Engine
              paramType: path
              type: string
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
        request_serializer: Nodes.Container.Service.serializers.ServiceEngineSerializer
        response_serializer: Nodes.Container.Service.serializers.ServiceEngineSerializer
        """
        serializer = ServiceEngineNestedSerializer(data=request.data, container_id=container_id)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ServiceEngineNestedDetail(APIView):
    
    def get(self, request, DPE_id, container_id, service_id, format=None):
        """
        Get the registration information of a Service Engine for specific container
        ---
        parameters:
            - name: DPE_id
              description: ID of DPE
              required: True
              paramType: path
              type: string
            - name: container_id
              description: ID of container
              required: True
              paramType: path
              type: string
            - name: service_id
              description: ID of service
              required: True
              paramType: path
              type: string
        response_serializer: Nodes.Container.Service.serializers.ServiceEngineSerializer
        """
        try:
            serv_object = Node.objects.get(node_id=DPE_id).containers.get(id=container_id).services.get(id=service_id)
            serializer = ServiceEngineSerializer(serv_object)
            return Response(serializer.data)            
        except Node.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Container.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
