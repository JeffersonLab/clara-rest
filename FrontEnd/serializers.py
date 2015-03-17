'''
Created on 11-03-2015

@author: royarzun
'''
from rest_framework import serializers

from Nodes.serializers import NodeSerializer
from models import FrontEnd


class FrontEndSerializer(serializers.ModelSerializer):
    nodes = NodeSerializer(many=True)

    class Meta:
        model = FrontEnd
        fields = ('hostname', 'celery_id', 'owner',
                  'created', 'status', 'nodes'
                  )
