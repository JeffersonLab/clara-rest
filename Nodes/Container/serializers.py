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
        fields = ('dpe_id', 'name','services')
