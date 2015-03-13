'''
Created on 13-03-2015

@author: royarzun
'''
from rest_framework import serializers

from models import Node

class NodeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Node
        fields = ('frontend', 'hostname', 'celery_id', 'created', 'status')