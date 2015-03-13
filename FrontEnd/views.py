from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from FrontEnd.serializers import FrontEndSerializer
from FrontEnd.models import FrontEnd
'''
FrontEnd Views:
Views for json responses for the Clara Frontend (PLATFORM) components
'''
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
    
@api_view(['GET', 'POST'])
def fe_list(request):
    """
    List all frontends, or create a new one.
    """
    if request.method == 'GET':
        fe_objects = FrontEnd.objects.all()
        serializer = FrontEndSerializer(fe_objects, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = FrontEndSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def fe_detail(request, nodeid):
    """
    Retrieve, update or delete a frontend.
    """
    try:
        fe_object = FrontEnd.objects.get(celery_id=nodeid)
    except FrontEnd.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = FrontEndSerializer(fe_object)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = FrontEndSerializer(fe_object, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        fe_object.delete()
        return HttpResponse(status=204)