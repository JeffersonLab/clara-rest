# coding=utf-8

from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.rest.Container.models import Container
from backend.rest.Container.serializers import ContainerSerializer
from backend.rest.DPE.models import DPE

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


class ContainersView(ListCreateAPIView):

    serializer_class = ContainerSerializer

    def get_queryset(self):
        queryset = Container.objects.all()
        container_name = self.request.query_params.get('name', None)

        if container_name:
            queryset = queryset.filter(name__iexact=container_name)
        return queryset

    def get(self, request, *args, **kwargs):
        """
        Get the registration information of a Clara Containers
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
        return super(ContainersView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Create a new Clara Container
        """
        if 'DPE_id' in kwargs:
            request.data['dpe_id'] = int(kwargs.pop('DPE_id'))

            try:
                dpe = DPE.objects.get(node_id=request.data['dpe_id'])
                container = Container(dpe=dpe, name=request.data['name'])
                container.save()
                return Response(data=ContainerSerializer(container).data,
                                status=status.HTTP_201_CREATED)

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
            claraweb.rest.DPE.serializers.DPESerializer
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
