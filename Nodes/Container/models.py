'''
Created on 24-03-2015

@author: royarzun
'''
from django.db import models
from datetime import datetime

from Nodes.models import Node


class Container(models.Model):
    dpe_id = models.ForeignKey(Node, related_name='containers')
    name = models.CharField(max_length=20, null=True)
    created = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.dpe_id.hostname)+":"+str(self.name)

    def save(self):
        if self.created is None:
            self.created = datetime.now()
        self.modified = datetime.now()
        super(Container, self).save()

    class Meta:
        ordering = ('created',)
