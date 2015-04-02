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


class ServiceEngineInfo(models.Model):
    dpe_id = models.IntegerField(null=True)
    container_id = models.ForeignKey(Container, related_name='services')
    service_class = models.CharField(max_length=50, null=True)
    threads = models.IntegerField(null=True)

    created = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.container_id)+":"+str(self.name)

    def save(self):
        if self.created is None:
            self.created = datetime.now()
        self.modified = datetime.now()
        super(ServiceEngineInfo, self).save()

    class Meta:
        ordering = ('created',)


class ServiceConfiguration(models.Model):
    options = models.TextField(default="[]")
