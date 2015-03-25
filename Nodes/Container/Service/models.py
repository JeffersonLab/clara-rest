'''
Created on 24-03-2015

@author: royarzun
'''
from django.db import models
from datetime import datetime

from Nodes.Container.models import Container


class Service(models.Model):
    container_id = models.ForeignKey(Container)
    service_class = models.CharField(max_length=50, null=True)
    created = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.container_id)+":"+str(self.name)

    def save(self):
        if self.created is None:
            self.created = datetime.now()
        self.modified = datetime.now()
        super(Service, self).save()

    class Meta:
        ordering = ('created',)
