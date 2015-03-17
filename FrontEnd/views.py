from django.http import Http404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from FrontEnd.serializers import FrontEndSerializer
from FrontEnd.models import FrontEnd
'''
FrontEnd Views:
Views for json responses for the Clara Frontend (PLATFORM) components
'''


class FrontEndList(APIView):
    """
    List all frontends, or create a new one.
    """
    def get(self, request, format=None):
        fe_objects = FrontEnd.objects.all()
        serializer = FrontEndSerializer(fe_objects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FrontEndSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FrontEndDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, feid):
        try:
            return FrontEnd.objects.get(celery_id=feid)
        except FrontEnd.DoesNotExist:
            raise Http404

    def get(self, request, feid, format=None):
        fe_object = self.get_object(feid)
        serializer = FrontEndSerializer(fe_object)
        return Response(serializer.data)

    def put(self, request, feid, format=None):
        fe_object = self.get_object(feid)
        serializer = FrontEndSerializer(fe_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, feid, format=None):
        fe_object = self.get_object(feid)
        fe_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)