'''
Created on 24-03-2015

@author: royarzun
'''
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from serializers import ContainerSerializer, ContainerNestedSerializer
from Nodes.models import Node
from models import Container
"""
Container views:
Views for json responses for the Clara Containers at Specific Hostname (DPE)
"""


class ContainerList(APIView):

    def get(self, request, DPE_id=None, format=None):
        """
        Find all containers
        """
        container_objects = Container.objects.all()
        serializer = ContainerSerializer(container_objects, many=True)
        return Response(serializer.data)

    def post(self, request, DPE_id=None, format=None):
        """
        Create a new Clara Container
        ---
        parameters:
            - name: dpe_id
              description: ID of DPE
              paramType: string
              type: string
            - name: name
              description: ID of container
              paramType: string
              type: string
        """
        serializer = ContainerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContainerDetail(APIView):

    def get_object(self, container_id):
        try:
            return Container.objects.get(container_id=container_id)
        except Container.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, container_id, format=None):
        """
        Get the registration information of a Clara Container using its id
        ---
        parameters:
            - name: container_id
              description: ID of container
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
            container_object = self.get_object(container_id)
            serializer = ContainerSerializer(container_object)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, container_id, format=None):
        """
        Delete an specific Container instance using its id
        ---
        parameters:
            - name: container_id
              description: ID of container
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
        try:
            container_object = self.get_object(container_id)
            container_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ContainerNestedList(APIView):

    def get(self, request, DPE_id, format=None):
        """
        Find all containers for determined dpe
        ---
        response_serializer: Nodes.Container.serializers.ContainerSerializer
        """
        try:
            container_objects = Node.objects.get(node_id=DPE_id).containers.all()
            serializer = ContainerSerializer(container_objects, many=True)
            if serializer:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, DPE_id, format=None):
        """
        Create a new Clara Container
        ---
        request_serializer: Nodes.Container.serializers.ContainerNestedSerializer
        """
        serializer = ContainerNestedSerializer(data=request.data,
                                               dpe=DPE_id)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContainerNestedDetail(APIView):

    def get_object(self, container_id):
        try:
            return Container.objects.get(container_id=container_id)
        except Container.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, container_id, DPE_id=None, format=None):
        """
        Get the registration information of a Clara Container using its id
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
            container_object = self.get_object(container_id)
            serializer = ContainerSerializer(container_object)
            return Response(serializer.data)
        except container_object.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, DPE_id, container_id, format=None):
        """
        Delete an specific Container instance using its id
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
            container_object = self.get_object(container_id)
            container_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
