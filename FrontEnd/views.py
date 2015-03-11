from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from FrontEnd.serializers import FrontEndSerializer
from FrontEnd.models import FrontEnd

#from tasks import start_fe_task, get_task_status, revoke_task
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
    
@csrf_exempt
def fe_list(self, request):
    """
    List all code snippets, or create a new snippet.
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

@csrf_exempt
def fe_detail(request, pk):
    """
    Retrieve, update or delete a frontend.
    """
    try:
        fe_object = FrontEnd.objects.get(pk=pk)
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
    
# def index(request):
#     data = serializers.serialize('json', FrontEnd.objects.filter(status='Active'), fields=('hostname','celery_id'))
#     data = json.dumps(json.loads(data), indent=4)
#     return HttpResponse(data, content_type="application/json")    
# 
# def show(request, feid,):
#     data = get_task_status(feid)
#     data = json.dumps(json.loads(data), indent=4)
#     return HttpResponse(data, content_type="application/json")
# 
# def create(request):
#     pid = start_fe_task.delay('Hello World!')
#     fe_object = FrontEnd()
#     fe_object.celery_id = pid
#     fe_object.ip = '127.0.0.1'
#     fe_object.status ='Active'
#     fe_object.save()
#     data = get_task_status(pid.id)
#     return HttpResponse(data, content_type="application/json")
# 
# def destroy(request, feid):
#     fe_object = FrontEnd.objects.get(celery_id=feid)
#     fe_object.status = 'Stopped'
#     fe_object.save()
#     revoke_task(feid)
#     return HttpResponse(json.dumps({'id' : feid, 'status' : 'DESTROYED'}))