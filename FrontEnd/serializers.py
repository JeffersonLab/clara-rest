'''
Created on 11-03-2015

@author: royarzun
'''
from rest_framework import serializers
from models import FrontEnd

class FrontEndSerializer(serializers.ModelSerializer):
#     hostname  = serializers.CharField(read_only=True)
#     celery_id = serializers.CharField(required=False, allow_blank=True, max_length=36)
#     created   = serializers.DateTimeField()
#     status    = serializers.CharField(required=False, default="PENDING")
    
    class Meta:
        model = FrontEnd
        fields = ('hostname', 'celery_id', 'created', 'status')

#     def create(self, validated_data):
#         return FrontEnd.objects.create(**validated_data)
#     
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `FrontEnd` instance, given the validated data.
#         """
#         instance.hostname  = validated_data.get('hostname', instance.title)
#         instance.celery_id = validated_data.get('celery_id', instance.code)
#         instance.created   = validated_data.get('created', instance.linenos)
#         instance.status    = validated_data.get('status', instance.language)
#         instance.save()
#         return instance