# coding=utf-8

from rest_framework import serializers

from models import ServiceEngine


class ServiceEngineSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceEngine
        fields = ('service_id', 'container', 'engine_name', 'class_name',
                  'author', 'version', 'description',)
        read_only_fields = ('service_id')
