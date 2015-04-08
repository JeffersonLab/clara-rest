'''
Created on 26-03-2015

@author: royarzun
'''
from django.http import Http404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from serializers import SubscriptionSerializer
from models import SubscriptionHandler
'''
Subscription Views:
Views for json responses for the Clara Subscription feature
'''


class SubscriptionList(APIView):
    
    def get(self, request, format=None):
        """
        List all Subscriptions
        ---

        """
        subs_objects = SubscriptionHandler.objects.all()
        serializer = SubscriptionSerializer(subs_objects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Create new subscription
        ---
        request_serializer: Subscription.serializers.SubscriptionSerializer
        response_serializer: Subscription.serializers.SubscriptionSerializer
        """
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionDetail(APIView):
    
    def get_object(self, subscription_id):
        try:
            return SubscriptionHandler.objects.get(subscription_id=subscription_id)
        except SubscriptionHandler.DoesNotExist:
            raise Http404

    def get(self, request, subscription_id, format=None):
        """
        Retrieve a subscription
        ---
        parameters:
            - name: subscription_id
              description: Id of the subscription
              paramType: path
              required: True
        response_serializer: Subscription.serializers.SubscriptionSerializer
        responseMessages:
            - code: 400
              message: Bad request
            - code: 401
              message: Not authenticated
            - code: 404
              message: Resource not found
        """
        sub_object = self.get_object(subscription_id)
        serializer = SubscriptionSerializer(sub_object)
        return Response(serializer.data)

    def delete(self, request, subscription_id, format=None):
        """
        Deletes a subscription
        ---
        parameters:
            - name: subscription_id
              description: Id of the subscription
              paramType: path
              required: True
        responseMessages:
            - code: 400
              message: Bad request
            - code: 401
              message: Not authenticated
            - code: 404
              message: Resource not found
        """
        sub_object = self.get_object(subscription_id)
        sub_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
