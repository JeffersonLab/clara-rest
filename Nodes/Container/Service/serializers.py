'''
Created on 13-03-2015

@author: royarzun
'''
from rest_framework import serializers

from Nodes.Container.models import Container
from models import ServiceEngine


# class ServiceConfigSerializer(serializers.Serializer):
#     option = serializers.CharField(max_length=50)
#     value = serializers.CharField(max_length=50)


class ServiceEngineSerializer(serializers.ModelSerializer):
    #configuration = ServiceConfigSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceEngine
        fields = ('service_id', 'container', 'engine_class', 'configuration', 'threads')
        read_only_fields = ('service_id', 'container', 'configuration', )


class ServiceEngineNestedSerializer(serializers.ModelSerializer):
    parent_id = None
    
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
        # TODO: Check what to do with empty configuration
        try:
            parent = Container.objects.get(container_id=self.parent_id)
            parent.services.add(service)
            service.save()
            parent.save()
            return service
        except:
            print service
            raise serializers.ValidationError("Container must be registered and available!")
