#
# Copyright (C) 2015. Jefferson Lab, Clara framework (JLAB). All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its
# documentation for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement.
#
# Author Ricardo Oyarzun
# Department of Experimental Nuclear Physics, Jefferson Lab.
#
# IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
# INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
# THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
#
# JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
# HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
# SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from ClaraNodes.Container.serializers import ContainerSerializer
from ClaraNodes.Container.Service.models import ServiceEngine
from ClaraNodes.Container.models import Container
from ClaraNodes.models import Node
"""
Container views:
Views for json responses for the Clara Containers at Specific Hostname (DPE)
"""


def find_container_object(container_id, dpe_id=None):
    try:
        if dpe_id:
            node = Node.objects.get(node_id=dpe_id)
            return node.containers.get(container_id=container_id)
        else:
            return Container.objects.get(container_id=container_id)

    except Container.DoesNotExist:
        return None

    except Node.DoesNotExist:
        return None


class ContainersView(APIView):

    def get(self, request):
        """
        Find all containers
        ---
        parameters:
            - name: filter_by_containername
              type: string
              paramType: query
              description: container name to filter containers
            - name: filter_by_servicename
              type: string
              paramType: query
              description: service name to filter containers
        responseMessages:
            - code: 401
              message: Not authenticated
        """
        container_filter = request.GET.get('filter_by_containername')
        service_filter = request.GET.get('filter_by_servicename')
        containers_data = Container.objects.all()

        if container_filter:
            containers_data = containers_data.filter(name__contains=container_filter)

        elif service_filter:
            filtered_services = ServiceEngine.objects.filter(engine_name__contains=service_filter)
            containers_data = containers_data.filter(services=filtered_services)

        serializer = ContainerSerializer(containers_data, many=True)
        return Response(serializer.data)


class ContainerView(APIView):

    def get(self, request, container_id):
        """
        Get the registration information of a Clara Container using its id
        ---
        parameters:
            - name: container_id
              description: ID of container
              required: True
              paramType: path
              type: string
        response_serializer:
            ClaraNodes.serializers.NodeSerializer
        responseMessages:
            - code: 400
              message: Bad request
            - code: 401
              message: Not authenticated
            - code: 404
              message: Resource not found
        """
        container_id = int(container_id)

        container_object = find_container_object(container_id)
        if container_object:
            serializer = ContainerSerializer(container_object)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, container_id):
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
        container_id = int(container_id)

        container_object = find_container_object(container_id)
        if container_object:
            container_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DpeContainersView(APIView):

    def get(self, request, DPE_id):
        """
        Find all containers for determined dpe
        ---
        parameters:
            - name: filter_by_containername
              type: string
              paramType: query
              description: container name to filter
            - name: filter_by_servicename
              type: string
              paramType: query
              description: containers containing service
        response_serializer:
            ClaraNodes.Container.serializers.ContainerSerializer
        responseMessages:
            - code: 400
              message: Bad request
            - code: 401
              message: Not authenticated
            - code: 404
              message: Resource not found
        """
        DPE_id = int(DPE_id)

        container_filter = request.GET.get('filter_by_containername')
        service_filter = request.GET.get('filter_by_servicename')
        containers_data = Node.objects.get(node_id=DPE_id).containers.all()

        if container_filter:
            containers_data = containers_data.filter(name__contains=container_filter)

        elif service_filter:
            filtered_services = ServiceEngine.objects.filter(engine_name__contains=service_filter)
            containers_data = containers_data.filter(services=filtered_services)

        serializer = ContainerSerializer(containers_data, many=True)
        return Response(serializer.data)

    def post(self, request, DPE_id):
        """
        Create a new Clara Container
        ---
        request_serializer:
            ClaraNodes.Container.serializers.ContainerNestedSerializer
        responseMessages:
            - code: 400
              message: Bad request
            - code: 401
              message: Not authenticated
            - code: 404
              message: Resource not found
        """
        DPE_id = int(DPE_id)

        serializer = ContainerSerializer(data=request.data)
        if serializer.is_valid():
            try:
                node_object = Node.objects.get(node_id=DPE_id)
                serializer.save(dpe=node_object)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)

            except Node.DoesNotExist:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DpeContainerView(APIView):

    def get(self, request, container_id, DPE_id=None):
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
        response_serializer:
            ClaraNodes.serializers.NodeSerializer
        responseMessages:
            - code: 400
              message: Bad request
            - code: 401
              message: Not authenticated
            - code: 404
              message: Resource not found
        """
        container_id = int(container_id)
        DPE_id = int(DPE_id)

        container_object = find_container_object(container_id, DPE_id)
        if container_object:
            serializer = ContainerSerializer(container_object)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, DPE_id, container_id):
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
        response_serializer: ClaraNodes.serializers.NodeSerializer
        responseMessages:
            - code: 400
              message: Bad request
            - code: 401
              message: Not authenticated
            - code: 404
              message: Resource not found
        """
        container_id = int(container_id)
        DPE_id = int(DPE_id)

        container_object = find_container_object(container_id, DPE_id)
        if container_object:
            container_object.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
