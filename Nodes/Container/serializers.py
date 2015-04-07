'''
Created on 13-03-2015

@author: royarzun
'''
from rest_framework import serializers

from Service.serializers import ServiceEngineSerializer
from Nodes.models import Node
from models import Container


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
    parent_id = None
    parent_dpe = None

    def __init__(self, *args, **kwargs):
        self.parent_id = kwargs.pop('dpe', None)
        super(ContainerNestedSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Container
        fields = ('container_id', 'dpe', 'name')
        read_only_fields = ('container_id', 'dpe')

    def create(self, validated_data):
        # TODO: Get the exception for not found
        container = Container(name=validated_data['name'])
        try:
            self.parent_dpe = Node.objects.get(node_id=self.parent_id)
            self.parent_dpe.containers.add(container)
            container.save()
            self.parent_dpe.save()
            return container
        except:
            raise serializers.ValidationError("DPE must be registered and available!")
