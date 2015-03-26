'''
Created on 26-03-2015

@author: royarzun
'''
from rest_framework import serializers

from models import SubscriptionHandler


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionHandler
        fields = ('subscription_id', 'type', 'sender', 'created', 'modified')
        read_only_fields = ('subscription_id', 'created', 'modified')

    def create(self, validated_data):
        subscription = SubscriptionHandler(
                                          type = validated_data['type'],
                                          sender = validated_data['sender']
                                          )
        subscription.save()
        return subscription
