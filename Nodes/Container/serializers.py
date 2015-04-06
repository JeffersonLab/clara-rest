'''
Created on 13-03-2015

@author: royarzun
'''
from rest_framework import serializers

from Service.serializers import ServiceEngineInfoSerializer
from Nodes.models import Node
from models import Container


class ContainerSerializer(serializers.ModelSerializer):
    services = ServiceEngineInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Container
        fields = ('id', 'dpe_id', 'name', 'services')
        read_only_fields = ('services', 'id')

    def create(self, validated_data):
        container = Container(dpe_id=validated_data['dpe_id'],
                              name=validated_data['name'])
        container.save()
        return container


class ContainerNestedSerializer(serializers.ModelSerializer):
    parent_id = None
    parent_dpe = None

    def __init__(self, *args, **kwargs):
        self.parent_id = kwargs.pop('dpe_id', None)
        super(ContainerNestedSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Container
        fields = ('id', 'dpe_id', 'name')
        read_only_fields = ('id', 'dpe_id')

    def create(self, validated_data):
        # TODO: Get the exception for not found
        container = Container(name=validated_data['name'])
        try:
            self.parent_dpe = Node.objects.get(node_id=self.parent_id)
            self.parent_dpe.containers.add(container)
        except:
            raise serializers.ValidationError("DPE must be registered and available!")
        container.save()
        self.parent_dpe.save()
        return container
