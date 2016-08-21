# coding=utf-8

from rest_framework import serializers

from claraweb.rest.DPE.models import DPE


class DPESerializer(serializers.ModelSerializer):
    canonical_name = serializers.SerializerMethodField()
    deployed_containers = serializers.SerializerMethodField()

    class Meta:
        model = DPE
        fields = ('node_id', 'canonical_name','hostname', 'language',
                  'n_cores', 'memory_size', 'deployed_containers',
                  'start_time', 'modified', )

    def get_canonical_name(self, obj):
        return str(obj)

    def get_deployed_containers(self, obj):
        return obj.containers.count()

    def create(self, validated_data):
        node = DPE(**validated_data)
        node.save()
        return node
