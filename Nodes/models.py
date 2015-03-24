from django.db import models
from datetime import datetime


class Node(models.Model):
    node_id = models.IntegerField(primary_key=True)
    hostname = models.IPAddressField()
    created = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)    

    def __str__(self):
        return self.hostname+"-"+str(self.created)

    def save(self):
        if self.created is None:
            self.created = datetime.now()
        self.modified = datetime.now()
        super(Node, self).save()

    class Meta:
        ordering = ('created',)
