#
# Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
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

from RuntimeDataRegistrar.models import DPESnapshot
from serializers import ServiceEngineSerializer, ServiceEngineNestedSerializer
from Nodes.models import Node
from Nodes.Container.models import Container
from models import ServiceEngine
"""
Services Views:
Views for json responses for the Clara ServiceEngines
"""


def get_node_object(DPE_id):
        try:
            return Node.objects.get(node_id=DPE_id)

        except Node.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND


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
        response_serializer:
            Nodes.Container.Service.serializers.ServiceEngineSerializer
        responseMessages:
            - code: 401
              message: Not authenticated
        """
        dpe_regex = request.GET.get('DPE_regex')
        container_regex = request.GET.get('container_regex')
        service_regex = request.GET.get('service_regex')
        if dpe_regex is not None:
            pass
        if container_regex is not None:
            pass
        if service_regex is not None:
            pass
        service_objects = ServiceEngine.objects.all()
        serializer = ServiceEngineSerializer(service_objects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Create a new service in one container at one DPE. The named container
        will be created if necessary.
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
            Nodes.Container.Service.serializers.ServiceEngineSerializer
        response_serializer:
            Nodes.Container.Service.serializers.ServiceEngineSerializer
        responseMessages:
            - code: 400
              message: Bad request
            - code: 401
              message: Not authenticated
        """
        serializer = ServiceEngineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceEngineNestedList(APIView):

    def get(self, request, DPE_id, container_id, format=None):
        """
        Get the registration information of the Service Engines for a specific
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
        response_serializer:
            Nodes.Container.Service.serializers.ServiceEngineSerializer
        responseMessages:
            - code: 400
              message: Bad request
            - code: 401
              message: Not authenticated
            - code: 404
              message: Resource not found
        """
        service_objects = ServiceEngine.objects.all()
        serializer = ServiceEngineSerializer(service_objects, many=True)
        return Response(serializer.data)

    def post(self, request, DPE_id, container_id, format=None):
        """
        Deploy a new service at Container. The name of the container will be
        created if is not provided.
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
        request_serializer:
            Nodes.Container.Service.serializers.ServiceEngineSerializer
        response_serializer:
            Nodes.Container.Service.serializers.ServiceEngineSerializer
        responseMessages:
            - code: 400
              message: Bad request
            - code: 401
              message: Not authenticated
            - code: 404
              message: Resource not found
        """
        serializer = ServiceEngineNestedSerializer(data=request.data)
        if serializer.is_valid():
            try:
                container_object = Container.objects.get(dpe=DPE_id,
                                                         container_id=container_id)
                serializer.save(container=container_object)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except Container.DoesNotExist:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceEngineNestedDetail(APIView):

    def get(self, request, DPE_id, container_id, service_id, format=None):
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
            Nodes.Container.Service.serializers.ServiceEngineSerializer
        responseMessages:
            - code: 400
              message: Bad request
            - code: 401
              message: Not authenticated
            - code: 404
              message: Resource not found
        """
        runtime_flag = request.GET.get('runtime')

        try:
            service_object = Node.objects.get(node_id=DPE_id).containers.get(container_id=container_id).services.get(service_id=service_id)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if runtime_flag:
            try:
                dpe_name = str(get_node_object(DPE_id))
                snap_group = DPESnapshot.objects.order_by('date').filter(name=dpe_name)
                snapshot = snap_group.order_by('date').last().get_data()

                print service_object.engine_name
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

            except KeyError as e:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                print e
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            serializer = ServiceEngineSerializer(service_object)
            return Response(serializer.data)
