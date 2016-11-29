# coding=utf-8

from django.core.exceptions import ValidationError
from rest_framework import serializers

from backend.rest.DPE.models import DPE
from backend.rest.Container.models import Container
from backend.rest.Service.serializers import ServiceEngineSerializer


def container_validator(container_id):
    """
    Check the existence of the respective parent node
    """
    try:
        DPE.objects.get(container_id=container_id)
    except DPE.DoesNotExist:
        raise ValidationError(u'DPE must be registered and available!')


class ContainerSerializer(serializers.ModelSerializer):
    services = ServiceEngineSerializer(many=True, read_only=True, required=False)
    dpe_id = serializers.SerializerMethodField()
    dpe_canonical_name = serializers.SerializerMethodField()
    canonical_name = serializers.SerializerMethodField()
    deployed_services = serializers.SerializerMethodField()

    class Meta:
        model = Container
        fields = ('dpe_id','container_id', 'dpe_canonical_name',
                  'canonical_name', 'name', 'deployed_services','services')
        write_only_fields = ('dpe', 'name',)
        read_only_fields = ('services', 'container_id', 'dpe_canonical_name',
                            'canonical_name',)

    def create(self, validated_data):
        return Container(**validated_data)

    def get_dpe_id(self, obj):
        return int(obj.dpe.node_id)

    def get_dpe_canonical_name(self, obj):
        return str(obj.get_dpe_name())

    def get_canonical_name(self, obj):
        return str(obj.get_canonical_name())

    def get_deployed_services(self, obj):
        return obj.services.count()
