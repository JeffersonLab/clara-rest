'''
Created on 09-04-2015

@author: royarzun
'''
from rest_framework import serializers

from models import App


class AppSerializer(serializers.ModelSerializer):

    class Meta:
        model = App
        fields = ('app_id', 'chain', 'registered_class', 'created', 'modified')
        read_only_fields = ('app_id', 'created', 'modified')

    def create(self, validated_data):
        app = App()
        app.save()
        return app
