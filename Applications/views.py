'''
Created on 08-04-2015

@author: royarzun
'''
from django.http import Http404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from serializers import AppSerializer
from models import App
'''
Application Views:
Views for json responses for the Clara Applications
'''


class AppList(APIView):
    
    def get(self, request, format=None):
        """
        List all Applications
        ---

        """
        app_objects = App.objects.all()
        serializer = AppSerializer(app_objects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Create new Clara Application
        ---
        request_serializer: Applications.serializers.AppSerializer
        response_serializer: Applications.serializers.AppSerializer
        """
        serializer = AppSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppDetail(APIView):
    
    def get_object(self, application_id):
        try:
            return App.objects.get(app_id=application_id)
        except App.DoesNotExist:
            raise Http404

    def get(self, request, application_id, format=None):
        """
        Retrieve an application
        ---
        parameters:
            - name: subscription_id
              description: Id of the subscription
              paramType: path
              required: True
        response_serializer: Applications.serializers.AppSerializer
        responseMessages:
            - code: 400
              message: Bad request
            - code: 401
              message: Not authenticated
            - code: 404
              message: Resource not found
        """
        app_object = self.get_object(application_id)
        serializer = AppSerializer(app_object)
        return Response(serializer.data)

    def delete(self, request, application_id, format=None):
        """
        Removes an application
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
        app_object = self.get_object(application_id)
        app_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)