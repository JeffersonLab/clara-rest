'''
Created on 13-03-2015

@author: royarzun
'''
from rest_framework import serializers

from models import Node


class NodeSerializer(serializers.ModelSerializer):


    class Meta:
        model = Node
        fields = ('hostname', 'node_id', 'created', 'modified')
        read_only_fields = ('node_id', 'created', 'modified')


    def create(self, validated_data):
        node = Node(hostname=validated_data['hostname'])
        node.save()
        return node
