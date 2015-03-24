'''
Created on 24-03-2015

@author: royarzun
'''
from django.db import models
from datetime import datetime

from Nodes.models import Node


class Container(models.Model):
    dpe_id = models.ForeignKey(Node)
    container_id = models.AutoField()
    created = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)

    def __str__(self):
        return "DPE:"+str(self.dpe_id)+"-Container:"+str(self.container_id)

    def save(self):
        if self.created is None:
            self.created = datetime.now()
        self.modified = datetime.now()
        super(Container, self).save()
    
    class Meta:
        ordering = ('created',)
