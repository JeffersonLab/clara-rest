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

from django.core.exceptions import ValidationError
from rest_framework import serializers

from Service.serializers import ServiceEngineSerializer
from Nodes.models import Node
from models import Container


def container_validator(container_id):
    """
    Check the existence of the respective parent node
    """
    try:
        Node.objects.get(container_id=container_id)
        print "DPE exists and its available"
    except Node.DoesNotExist:
        raise ValidationError(u'DPE must be registered and available!')
    

class ContainerSerializer(serializers.ModelSerializer):
    services = ServiceEngineSerializer(many=True, read_only=True)

    class Meta:
        model = Container
        fields = ('container_id', 'dpe', 'name', 'services')
        read_only_fields = ('services', 'container_id')

    def create(self, validated_data):
        container = Container(dpe=validated_data['dpe'],
                              name=validated_data['name'])
        container.save()
        return container


class ContainerNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Container
        fields = ('container_id', 'dpe', 'name')
        read_only_fields = ('container_id', 'dpe')

    def create(self, validated_data):
        container = Container(dpe=validated_data['dpe'],
                              name=validated_data['name'])
        container.save()
        return container
