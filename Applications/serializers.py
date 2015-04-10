'''
Created on 09-04-2015

@author: royarzun
'''
from rest_framework import serializers

from models import App, Chain


class ChainSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Chain
        fields = ('app', 'services')
        read_only_fields =('app', )

class AppSerializer(serializers.ModelSerializer):
    chain = ChainSerializer(many=False, read_only=False)

    class Meta:
        model = App
        fields = ('app_id', 'registered_class', 'chain', 'input', 'output', 'created', 'modified')
        read_only_fields = ('app_id', 'created', 'modified')

    def create(self, validated_data):
        chain_data = validated_data.pop('chain')
        app_object = App(registered_class=validated_data['registered_class'],
                         input=validated_data['input'],
                         output=validated_data['output'])
        app_object.save()
        Chain.objects.create(app=app_object,**chain_data)
        return app_object
