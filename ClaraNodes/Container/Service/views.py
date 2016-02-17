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

from ClaraDataRegistrar.models import DPESnapshot
from ClaraNodes.Container.Service.serializers import *
from ClaraNodes.Container.Service.models import ServiceEngine
from ClaraNodes.Container.models import Container
from ClaraNodes.models import Node
"""
Services Views:
Views for json responses for the Clara ServiceEngines
"""
def find_parents(container_id, dpe_id=None):
    try:
        if dpe_id:
            node = Node.objects.get(node_id=int(dpe_id))
            return node.containers.get(container_id=int(container_id))
        else:
            return Container.objects.get(container_id=int(container_id))

    except Container.DoesNotExist:
        return None

    except Node.DoesNotExist:
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
            ClaraNodes.Container.Service.serializers.ServiceEngineSerializer
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
            ClaraNodes.Container.Service.serializers.ServiceEngineSerializer
        response_serializer:
            ClaraNodes.Container.Service.serializers.ServiceEngineSerializer
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

    def get(self,request, service_id, container_id=None, DPE_id=None):
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
            ClaraNodes.Container.Service.serializers.ServiceEngineSerializer
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
        else:
            container_parent = find_parents(request.data('container'), DPE_id)

        if not container_parent:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        service_object = container_parent.services.get(service_id=service_id)

        runtime_flag = request.GET.get('runtime')
        if runtime_flag:
            try:
                dpe_name = str(service_object.container.dpe_id)
                snap_group = DPESnapshot.objects.order_by('date').filter(name=dpe_name)
                snapshot = snap_group.order_by('date').last().get_data()

                for c in snapshot['DPERuntime']['containers']:
                    for s in c['ContainerRuntime']['services']:
                        if s['ServiceRuntime']['name'] == service_object.engine_name:
                            s_run_data = s['ServiceRuntime']

                if runtime_flag == "all":
                    return Response(s_run_data)

                else:
                    return Response({'dpe': dpe_name,
                                     'dpe_id': DPE_id,
                                     'container_id': container_id,
                                     'service_id': service_id,
                                     'snapshot_time': s_run_data['snapshot_time'],
                                     runtime_flag: s_run_data[runtime_flag]})

            except KeyError:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            except Exception:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            serializer = ServiceEngineSerializer(service_object)
            return Response(serializer.data)
