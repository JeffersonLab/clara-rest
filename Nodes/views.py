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

from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from RuntimeDataRegistrar.models import DPESnapshot
from Nodes.serializers import NodeSerializer
from Nodes.Container.Service.models import ServiceEngine
from Nodes.Container.models import Container
from Nodes.models import Node
"""
Nodes Views:
Views for json responses for the Clara Nodes (DPE) components
"""


def find_node_object(DPE_id):
    try:
        return Node.objects.get(node_id=DPE_id)

    except Node.DoesNotExist:
        raise Http404("Dpe not found!")


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
        name_filter = request.GET.get('filter_by_name')
        cores_filter = request.GET.get('filter_by_cores')
        mem_filter = request.GET.get('filter_by_memory')
        container_filter = request.GET.get('filter_by_containername')
        service_filter = request.GET.get('filter_by_servicename')
        nodes_data = Node.objects.all()

        if name_filter:
            nodes_data = nodes_data.filter(hostname__contains=name_filter)

        elif cores_filter:
            nodes_data = nodes_data.filter(n_cores=cores_filter)

        elif mem_filter:
            nodes_data = nodes_data.filter(memory_size=mem_filter)

        elif container_filter:
            filtered_containers = Container.objects.filter(name__contains=container_filter)
            nodes_data = Node.objects.filter(containers=filtered_containers)

        elif service_filter:
            filtered_services = ServiceEngine.objects.filter(engine_name__contains=service_filter)
            filtered_containers = Container.objects.filter(services=filtered_services)
            nodes_data = Node.objects.filter(containers=filtered_containers)

        serializer = NodeSerializer(nodes_data, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Start new DPE(s)
        ---
        parameters_strategy:
            form: replace
        parameters:
            - name: DPEInfo
              type: string
              description: Quantity and types of DPEs to start
            - name: hostname
              type: string
              description: hostname of the DPE to register
            - name: language
              type: string
              description: programming language of the DPE to register
            - name: n_cores
              type: int
              description: number of cores of the DPE to register
        response_serializer: Nodes.serializers.NodeSerializer
        responseMessages:
            - code: 400
              message: Bad Request
            - code: 401
              message: Not authenticated
        """
        serializer = NodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        response_serializer:
            Nodes.serializers.NodeSerializer
        responseMessages:
            - code: 400
              message: Bad request
            - code: 401
              message: Not authenticated
            - code: 404
              message: Resource not found
        """
        DPE_id = int(DPE_id)

        runtime_flag = request.GET.get('runtime')

        node_object = find_node_object(DPE_id)

        if runtime_flag:
            try:
                dpe_name = node_object.hostname
                snapshots = DPESnapshot.objects.order_by('date').filter(name=dpe_name)
                snapshot = snapshots.order_by('date').last().get_data()['DPERuntime']

                if runtime_flag == "all":
                    return Response(snapshot)

                else:
                    return Response({'dpe_id': DPE_id,
                                     'host': dpe_name,
                                     'snapshot_time': snapshot['snapshot_time'],
                                     runtime_flag: snapshot[runtime_flag]})
            except KeyError:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                print e
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            serializer = NodeSerializer(node_object)
            return Response(serializer.data)

    def delete(self, request, DPE_id):
        """
        Shutdown a Dpe
        ---
        parameters:
            - name: DPE_id
              description: ID of DPE
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
        DPE_id = int(DPE_id)

        node_object = find_node_object(DPE_id)
        node_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
