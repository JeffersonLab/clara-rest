'''
Created on 13-03-2015

@author: royarzun
'''
from rest_framework import serializers
from Nodes.Container.Service.models import ServiceEngineInfo


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceEngineInfo
        fields = ('service_class', 'container_id',)
