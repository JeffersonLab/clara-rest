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
    chain = ChainSerializer(many=False)

    class Meta:
        model = App
        fields = ('app_id', 'registered_class', 'chain', 'created', 'modified')
        read_only_fields = ('app_id', 'created', 'modified')

    def create(self, validated_data):
        app = App(validated_data)
        app.save()
        return app
