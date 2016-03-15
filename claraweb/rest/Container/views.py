# coding=utf-8

from claraweb.rest.Container.models import Container
from claraweb.rest.Container.serializers import ContainerSerializer
from claraweb.rest.DPE.models import DPE
from claraweb.rest.Service.models import ServiceEngine
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
"""
Container views:
Views for json responses for the Clara Containers at Specific Hostname (DPE)
"""


def find_container_object(container_id, dpe_id=None):
    try:
        if dpe_id:
            node = DPE.objects.get(node_id=dpe_id)
            return node.containers.get(container_id=container_id)
        else:
            return Container.objects.get(container_id=container_id)

    except Container.DoesNotExist:
        return None

    except DPE.DoesNotExist:
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
            containers_data = DPE.objects.get(node_id=DPE_id).containers

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
            claraweb.Container.serializers.ContainerSerializer
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
                node, created = DPE.objects.get(node_id=DPE_id).containers.get_or_create(**request.data)
                if created:
                    node.save()
                    return Response(status=status.HTTP_201_CREATED)

                else:
                    return Response(status=status.HTTP_200_OK)

            else:
                node = DPE.objects.get(node_id=request.data.pop('dpe'))
                container, created = node.containers.get_or_create(**request.data)

                if created:
                    container.save()
                    return Response(status=status.HTTP_201_CREATED)

                else:
                    return Response(status=status.HTTP_200_OK)

        except DPE.DoesNotExist:
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
            claraweb.serializers.NodeSerializer
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
