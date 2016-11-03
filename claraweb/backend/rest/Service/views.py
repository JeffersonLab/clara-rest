# coding=utf-8

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from claraweb.backend.rest.Container.models import Container
from claraweb.backend.rest.DPE.models import DPE
from claraweb.backend.rest.Service.serializers import *
"""
Services Views:
Views for json responses for the Clara ServiceEngines
"""


def find_parents(container_id, dpe_id=None):
    try:
        if dpe_id:
            node = DPE.objects.get(node_id=int(dpe_id))
            return node.containers.get(container_id=int(container_id))
        else:
            return Container.objects.get(container_id=int(container_id))

    except Container.DoesNotExist:
        return None

    except DPE.DoesNotExist:
        return None


class ServicesView(APIView):

    def get(self, request, container_id=None, DPE_id=None):
        """
        Find services that match the optional query parameters.<br>
        For all services omit the parameters.
        ---
        parameters:
            - name: filter_by_description
              type: string
              paramType: query
              description: filter services by description
              required: False
            - name: filter_by_name
              type: string
              paramType: query
              description: filter services by name
              required: False
            - name: filter_by_author
              type: string
              paramType: query
              description: filter services by author
              required: False
            - name: filter_by_language
              type: string
              paramType: query
              description: filter services by language
              required: False
        response_serializer:
            claraweb.rest.Service.serializers.ServiceEngineSerializer
        responseMessages:
            - code: 401
              message: Not authenticated
        """
        desc_filter = request.GET.get('filter_by_description')
        name_filter = request.GET.get('filter_by_servicename')
        lang_filter = request.GET.get('filter_by_language')
        auth_filter = request.GET.get('filter_by_author')


        if container_id:
            container = find_parents(container_id=container_id, dpe_id=DPE_id)
            services_data = container.services
        else:
            services_data = ServiceEngine.objects.all()

        if services_data:
            if desc_filter:
                services_data = services_data.filter(description__contains=desc_filter)

            elif name_filter:
                services_data = services_data.filter(engine_name__contains=name_filter)

            elif lang_filter:
                services_data = services_data.filter(language__contains=lang_filter)

            elif auth_filter:
                services_data = services_data.filter(author__contains=auth_filter)

            serializer = ServiceEngineSerializer(services_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, container_id=None, DPE_id=None):
        """
        Create a new service in one container at one DPE.
        ---
        parameters:
            - name: container_id
              description: Container Id for the Service Engine
              required: True
            - name: engine_name
              description: Service Engine canonical name
              required: True
            - name: class_name
              description: Name of class
              required: True
        request_serializer:
            claraweb.rest.Service.serializers.ServiceEngineSerializer
        response_serializer:
            claraweb.rest.Service.serializers.ServiceEngineSerializer
        responseMessages:
            - code: 400
              message: Bad request
            - code: 401
              message: Not authenticated
        """

        if 'container' in request.data:
            container_object = find_parents(container_id=request.data.pop('container'))

        else:
            container_object = find_parents(container_id=container_id, dpe_id=DPE_id)

        if container_object:
            service, created = ServiceEngine.objects.get_or_create(container=container_object,
                                                                   **request.data)
            if created:
                service.save()
                return Response(status=status.HTTP_201_CREATED)

            else:
                return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ServiceView(APIView):

    def get(self, request, service_id, container_id=None, DPE_id=None):
        """
        Get the registration information of a Service Engine for specific
        container
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
        response_serializer:
            claraweb.rest.Service.serializers.ServiceEngineSerializer
        responseMessages:
            - code: 400
              message: Bad request
            - code: 401
              message: Not authenticated
            - code: 404
              message: Resource not found
        """

        if container_id:
            container_parent = find_parents(container_id, DPE_id)
            if container_parent:
                service_object = container_parent.services.get(service_id=service_id)
                serializer = ServiceEngineSerializer(service_object)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        elif 'container' in request.data:
            container_parent = find_parents(request.data.pop('container'), DPE_id)
            if container_parent:
                service_object = container_parent.services.get(service_id=service_id)
                serializer = ServiceEngineSerializer(service_object)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if service_id:
                service_object = ServiceEngine.objects.get(service_id=service_id)

                if service_object:
                    serializer = ServiceEngineSerializer(service_object)
                    return Response(serializer.data)

                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
