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
from Nodes.serializers import NodeSerializer
from Nodes.models import Node
from hgext.extdiff import snapshot
"""
Nodes Views:
Views for json responses for the Clara Nodes (DPE) components
"""


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
        # TODO: Regex filters
        dpe_regex = request.GET.get('DPE_regex')
        container_regex = request.GET.get('container_regex')
        service_regex = request.GET.get('service_regex')

        serializer = NodeSerializer(Node.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
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

    def get_object(self, DPE_id):
        try:
            return Node.objects.get(node_id=DPE_id)

        except Node.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

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
        runtime_flag = request.GET.get('runtime')

        node_object = self.get_object(DPE_id)

        if runtime_flag:
            try:
                dpe_name = str(node_object)
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
        node_object = self.get_object(DPE_id)
        node_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
