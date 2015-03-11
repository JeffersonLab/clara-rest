from django.db import models
from FrontEnd.models import FrontEnd

from xsys.xMsgNode import xMsgNode
from datetime import datetime

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

    def new_node(self):
        node = xMsgNode()
        node.__init__()