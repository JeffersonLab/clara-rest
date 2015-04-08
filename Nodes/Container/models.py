'''
Created on 24-03-2015

@author: royarzun
'''
from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime

from Nodes.models import Node


def validate_node_existence(node_id):
    try:
        Node.objects.get(node_id=node_id)
    except Node.DoesNotExist:
        raise ValidationError(u'Dpe node must be registered and available')

class Container(models.Model):
    container_id = models.AutoField(primary_key=True, null=False)
    dpe = models.ForeignKey(Node, related_name='containers', validators=[validate_node_existence])
    name = models.CharField(max_length=20, null=True)
    created = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.dpe.hostname)+":"+str(self.name)

    def save(self):
        if self.created is None:
            self.created = datetime.now()
        self.modified = datetime.now()
        super(Container, self).save()

    class Meta:
        ordering = ('created',)
