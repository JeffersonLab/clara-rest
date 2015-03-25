'''
Created on 13-03-2015

@author: royarzun
'''
from rest_framework import serializers

from Container.serializers import ContainerSerializer
from models import Node


class NodeSerializer(serializers.ModelSerializer):
    containers = ContainerSerializer(many=True, read_only=True)

    class Meta:
        model = Node
        fields = ('hostname','node_id','containers')
