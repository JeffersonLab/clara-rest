from django.db import models
from datetime import datetime

from FrontEnd.models import FrontEnd


class Node(models.Model):
    frontend = models.ForeignKey(FrontEnd, related_name='nodes')
    hostname = models.IPAddressField(null=True)
    celery_id = models.CharField(max_length=36)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    status = models.CharField(max_length=15)

    def __str__(self):
        info_hosts = str(self.frontend.hostname)+":"+self.hostname
        info_status = str(self.status).upper()+"-"+str(self.created)
        return info_hosts+"-"+info_status

    def save(self):
        if self.created is None:
            self.created = datetime.now()
        self.modified = datetime.now()
        super(Node, self).save()

    class Meta:
        ordering = ('created',)
