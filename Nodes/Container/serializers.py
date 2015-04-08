'''
Created on 13-03-2015

@author: royarzun
'''
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
        return container
