'''
Created on 31-03-2015

@author: royarzun
'''
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from serializers import ServiceSerializer
from models import ServiceEngineInfo
"""
Services Views:
Views for json responses for the Clara Services
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
              in: query
              paramType: string
              description: Regular expression of the DPE id
              required: False
            - name: service_regex
              type: string
              located: query
              description: Regular expression of the DPE id
              required: False
        """
        service_objects = ServiceEngineInfo.objects.all()
        serializer = ServiceSerializer(service_objects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Create a new service in one container at one DPE. The named container will be created if necessary.
        ---
        parameters:
            - name: DPEInfo
              type: string
              description: Quantity and types of DPEs to start
        """
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
