'''
Created on 13-03-2015

@author: royarzun
'''
from rest_framework import serializers
from models import ServiceEngineInfo


class ServiceConfigSerializer(serializers.Serializer):
    option = serializers.CharField(max_length=50)
    value = serializers.CharField(max_length=50)


class ServiceEngineInfoSerializer(serializers.ModelSerializer):
    configuration = ServiceConfigSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceEngineInfo
        fields = ('container_id', 'engine_class', 'configuration', 'threads')
        read_only_fields = ('configuration', ) 
