'''
Created on 13-03-2015

@author: royarzun
'''
from rest_framework import serializers

from models import ServiceEngine


class ServiceEngineSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceEngine
        fields = ('service_id', 'container', 'engine_class', 'configuration', 'threads')
        read_only_fields = ('service_id', 'container', 'configuration', )


class ServiceEngineNestedSerializer(serializers.ModelSerializer):
    parent_id = None
    parent_dpe_id = None
    
    def __init__(self, *args, **kwargs):
        self.parent_id = kwargs.pop('container', None)
        super(ServiceEngineNestedSerializer, self).__init__(*args, **kwargs)
    
    class Meta:
        model = ServiceEngine
        fields = ('container', 'engine_class', 'configuration', 'threads')
        read_only_fields = ('container',)
        
    def create(self, validated_data):
        service = ServiceEngine(engine_class=validated_data['engine_class'],
                                threads=validated_data['threads'],
                                configuration=validated_data['configuration'])    
        return service
