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

from clara.DPE.models import Node
from clara.Service.models import ServiceEngine
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from clara.rest.Container import Container
from clara.rest.Container import ContainerSerializer

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

    def get(self, request, DPE_id=None):
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

        if DPE_id:
            containers_data = Node.objects.get(node_id=DPE_id).containers

        else:
            containers_data = Container.objects.all()

        if container_filter:
            containers_data = containers_data.filter(name__contains=container_filter)

        elif service_filter:
            filtered_services = ServiceEngine.objects.filter(engine_name__contains=service_filter)
            containers_data = containers_data.filter(services=filtered_services)

        serializer = ContainerSerializer(containers_data, many=True)
        return Response(serializer.data)

    def post(self, request, DPE_id=None):
        """
        Create a new Clara Container
        ---
        request_serializer:
            clara.Container.serializers.ContainerSerializer
        responseMessages:
            - code: 400
              message: Bad request
            - code: 401
              message: Not authenticated
            - code: 404
              message: Resource not found
        """

        try:
            if DPE_id:
                node, created = Node.objects.get(node_id=DPE_id).containers.get_or_create(**request.data)
                if created:
                    node.save()
                    return Response(status=status.HTTP_201_CREATED)

                else:
                    return Response(status=status.HTTP_200_OK)

            else:
                node = Node.objects.get(node_id=request.data.pop('dpe'))
                container, created = node.containers.get_or_create(**request.data)

                if created:
                    container.save()
                    return Response(status=status.HTTP_201_CREATED)

                else:
                    return Response(status=status.HTTP_200_OK)

        except Node.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ContainerView(APIView):

    def get(self, request, container_id, DPE_id=None):
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
            clara.serializers.NodeSerializer
        responseMessages:
            - code: 400
              message: Bad request
            - code: 401
              message: Not authenticated
            - code: 404
              message: Resource not found
        """
        container_id = int(container_id)

        container_object = find_container_object(container_id, DPE_id)
        if container_object:
            serializer = ContainerSerializer(container_object)
            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, container_id, DPE_id=None):
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

        container_object = find_container_object(container_id, dpe_id=DPE_id)
        if container_object:
            container_object.delete()
            return Response(status=status.HTTP_202_ACCEPTED)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
