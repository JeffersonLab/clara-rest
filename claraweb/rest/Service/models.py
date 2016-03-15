# coding=utf-8

from django.db import models

from claraweb.rest.Container.models import Container
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
    class_name = models.CharField(blank=False, max_length=40)
    engine_name = models.TextField(blank=True, default="")

    author = models.CharField(blank=False, max_length=40)
    version = models.CharField(blank=False, max_length=40)
    description = models.CharField(blank=False, max_length=100)

    start_time = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)

    class Meta:
        unique_together = ('container', 'engine_name' )

    def __str__(self):
        return "%s:%s" % (self.container.get_canonical_name(), self.engine_name)

    def get_canonical_name(self):
        return str(self)
