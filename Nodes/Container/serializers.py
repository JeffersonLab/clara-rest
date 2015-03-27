'''
Created on 13-03-2015

@author: royarzun
'''
from rest_framework import serializers

from Service.serializers import ServiceSerializer
from models import Container


class ContainerSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True) 

    class Meta:
        model = Container
        fields = ('id', 'dpe_id', 'name', 'services')
        read_only_fields = ('services', 'id')
        

    def create(self, validated_data):
        container = Container(
                              dpe_id = validated_data['dpe_id'],
                              name = validated_data['name']
                            )
        container.save()
        return container
