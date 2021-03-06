# coding=utf-8

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.rest.Container.models import Container
from backend.rest.DPE.models import DPE
from backend.rest.DPE.serializers import DPESerializer
from backend.rest.Service.models import ServiceEngine

"""
claraweb Views:
Views for json responses for the Clara claraweb (DPE) components
"""


def find_node_object(DPE_id):
    try:
        return DPE.objects.get(node_id=DPE_id)

    except DPE.DoesNotExist:
        return None


class Dpes(APIView):

    def get(self, request):
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
        name_filter = request.GET.get('name')
        cores_filter = request.GET.get('cores')
        mem_filter = request.GET.get('memory')
        container_filter = request.GET.get('containername')
        service_filter = request.GET.get('servicename')

        nodes_data = DPE.objects.all()

        if name_filter:
            nodes_data = nodes_data.filter(hostname__contains=name_filter)

        elif cores_filter:
            nodes_data = nodes_data.filter(n_cores=cores_filter)

        elif mem_filter:
            nodes_data = nodes_data.filter(memory_size=mem_filter)

        elif container_filter:
            filtered_containers = Container.objects.filter(name__contains=container_filter)
            nodes_data = DPE.objects.filter(containers=filtered_containers)

        elif service_filter:
            filtered_services = ServiceEngine.objects.filter(engine_name__contains=service_filter)
            filtered_containers = Container.objects.filter(services=filtered_services)
            nodes_data = DPE.objects.filter(containers=filtered_containers)

        serializer = DPESerializer(nodes_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Dpe(APIView):

    def get(self, request, DPE_id):
        """
        Retrieve, update or delete a DPE instance.
        ---
        parameters:
            - name: DPE_id
              description: ID of DPE
              required: True
              paramType: path
              type: string
            - name: runtime
              type: string
              paramType: query
              description: Regular expression of DPE ID
        response_serializer: claraweb.rest.DPE.serializers.DPESerializer
        responseMessages:
            - code: 400
              message: Bad request
            - code: 401
              message: Not authenticated
            - code: 404
              message: Resource not found
        """
        node_object = find_node_object(int(DPE_id))
        if node_object:
            serializer = DPESerializer(node_object)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
