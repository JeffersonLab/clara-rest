from django.db import models
from datetime import datetime

from FrontEnd.models import FrontEnd

class Node(models.Model):
    frontend  = models.ForeignKey(FrontEnd)
    hostname  = models.IPAddressField(null=True)
    celery_id = models.CharField(max_length=36)
    created   = models.DateTimeField()
    modified  = models.DateTimeField()
    status    = models.CharField(max_length=15) #Status of the Node ('Active', 'Stopped')        

    def save(self):
        if self.created == None:
            self.created = datetime.now()
        self.modified = datetime.now()
        super(Node, self).save()

    class Meta:
        ordering = ('created',)