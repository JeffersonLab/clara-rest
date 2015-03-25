'''
Created on 06-03-2015

@author: royarzun
'''
from django.db import models
from datetime import datetime


class Node(models.Model):
    node_id = models.AutoField(primary_key=True)
    hostname = models.IPAddressField()
    created = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)

    def __str__(self):
        return self.hostname

    def save(self):
        if self.created is None:
            self.created = datetime.now()
        self.modified = datetime.now()
        super(Node, self).save()

    class Meta:
        ordering = ('hostname',)
