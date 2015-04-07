'''
Created on 24-03-2015

@author: royarzun
'''
from django.db import models
from datetime import datetime

from Nodes.Container.models import Container

"""
A CLARA service engine runs in one container at one DPE.<br>
Must be threadsafe. Must implement CLARA service engine interface.
"""


class ServiceEngine(models.Model):
    """
    A CLARA service engine runs in one container at one DPE.
    Must be threadsafe. Must implement CLARA service engine interface.
    """
    service_id = models.AutoField(primary_key=True)
    container = models.ForeignKey(Container, related_name='services')
    engine_class = models.CharField(max_length=50, null=True)
    configuration = models.TextField(default="")
    # Number of threads that may be created to process messages 
    # for this single service instance
    threads = models.IntegerField(null=True)

    created = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.container)+":"+str(self.engine_class)

    def save(self):
        if self.created is None:
            self.created = datetime.now()
        self.modified = datetime.now()
        super(ServiceEngine, self).save()

    class Meta:
        ordering = ('created',)
