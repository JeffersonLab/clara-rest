'''
Created on 11-03-2015

@author: royarzun
'''
from rest_framework import serializers
from models import FrontEnd

class FrontEndSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FrontEnd
        fields = ('hostname', 'celery_id', 'created', 'status')