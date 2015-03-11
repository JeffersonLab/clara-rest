from django.core import serializers 
from django.db import models
from datetime import datetime


class FrontEnd(models.Model):
    hostname  = models.IPAddressField(null=True)
    celery_id = models.CharField(max_length=36) #FE id at the celery task queue
    created   = models.DateTimeField()
    modified  = models.DateTimeField()
    status    = models.CharField(max_length=15) #Status of the FE ('Active', 'Stopped')

    
    def save(self):
        if self.created == None:
            self.created = datetime.now()
        self.modified = datetime.now()
        super(FrontEnd, self).save()
    
    def to_json(self):
        JSONSerializer = serializers.get_serializer("json")
        xml_serializer = JSONSerializer()
        xml_serializer.serialize([self])
        data = xml_serializer.getvalue()
        return data
    