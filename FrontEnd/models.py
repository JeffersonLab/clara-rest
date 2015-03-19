from django.db import models
from datetime import datetime


class FrontEnd(models.Model):
    hostname = models.IPAddressField(null=True)
    celery_id = models.CharField(max_length=36)
    owner = models.ForeignKey('auth.User', related_name='frontends')
    created = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)
    status = models.CharField(default="Active", max_length=15)

    def __str__(self):
        return self.hostname+"-"+str(self.status).upper()+"-"+str(self.created)

    def save(self):
        if self.created is None:
            self.created = datetime.now()
        self.modified = datetime.now()
        super(FrontEnd, self).save()

    class Meta:
        ordering = ('created',)
