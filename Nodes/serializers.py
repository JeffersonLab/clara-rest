'''
Created on 13-03-2015

@author: royarzun
'''
from django.core.exceptions import ValidationError
from rest_framework import serializers

from models import Node

DPE_CREATION_LIMIT = 100


def limit_validator(value):
    if value > DPE_CREATION_LIMIT:
        raise ValidationError(u'%s bigger than the DPE creation limit' % value)


class NodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Node
        fields = ('hostname', 'node_id', 'created', 'modified')
        read_only_fields = ('node_id', 'created', 'modified')

    def create(self, validated_data):
        # TODO: Need to rethink about parameters for creation.
        # TODO: Figure who is in charge of assign the DPE Resources
        node = Node(hostname=validated_data['hostname'])
        node.save()
        return node


class NodeDeployerSerializer(serializers.Serializer):
    # TODO: Maybe we should think about bounds?
    DPEInfo = serializers.IntegerField(default=1, validators=[limit_validator])
