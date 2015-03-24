'''
Created on 13-03-2015

@author: royarzun
'''
from rest_framework import serializers
from models import Container


class ContainerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Container
