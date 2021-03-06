# coding=utf-8

from django.db import models
from datetime import datetime


class DPE(models.Model):
    node_id = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=40, blank=False)
    language = models.CharField(blank=False, max_length=20)
    n_cores = models.IntegerField(blank=False)
    memory_size = models.BigIntegerField(blank=False)
    clara_home = models.CharField(max_length=60)

    start_time = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)

    class Meta:
        managed = True

    def __str__(self):
        return self.hostname

    def __int__(self):
        return int(self.node_id)

    def get_host(self):
        return str(self.hostname.split("_")[0])

    def get_proxy_port(self):
        # Just for now hardcoded
        return 7771

    def save(self, *args, **kwargs):
        if self.start_time:
            self.modified = datetime.now()
        else:
            self.start_time = datetime.now()
            self.modified = datetime.now()
        super(DPE, self).save(*args, **kwargs)
