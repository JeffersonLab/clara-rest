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

from django.core.exceptions import ValidationError
from rest_framework import serializers

from clara.Container.Service.serializers import ServiceEngineSerializer
from clara.Container.models import Container
from clara.models import Node


def container_validator(container_id):
    """
    Check the existence of the respective parent node
    """
    try:
        Node.objects.get(container_id=container_id)
    except Node.DoesNotExist:
        raise ValidationError(u'DPE must be registered and available!')


class ContainerSerializer(serializers.ModelSerializer):
    services = ServiceEngineSerializer(many=True, read_only=True, required=False)
    dpe_id = serializers.SerializerMethodField()
    dpe_canonical_name = serializers.SerializerMethodField()
    canonical_name = serializers.SerializerMethodField()
    deployed_services = serializers.SerializerMethodField()

    class Meta:
        model = Container
        fields = ('dpe_id','container_id', 'dpe_canonical_name', 'canonical_name',
                  'name', 'deployed_services','services')
        write_only_fields = ('dpe', 'name')
        read_only_fields = ('services', 'container_id', 'dpe_canonical_name',
                            'canonical_name')

    def create(self, validated_data):
        return Container(**validated_data)

    def get_dpe_id(self, obj):
        return int(obj.dpe.node_id)

    def get_dpe_canonical_name(self, obj):
        return str(obj.get_dpe_name())

    def get_canonical_name(self, obj):
        return str(obj.get_canonical_name())

    def get_deployed_services(self, obj):
        return obj.services.count()
