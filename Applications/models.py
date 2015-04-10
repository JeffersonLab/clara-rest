'''
Created on 08-04-2015

@author: royarzun
'''
from django.db import models
from datetime import datetime


class App(models.Model):
    app_id = models.AutoField(primary_key=True)
    registered_class = models.CharField(max_length=50, default="")
    input = models.FilePathField(path="/work/input/", match="*.bin", default="")
    output = models.FilePathField(path="/work/output/", match="*.bin", default="")
    created = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)
    
    def __str__(self):
        return str(self.registered_class)+"_"+str(self.app_id)

    def save(self):
        if self.created is None:
            self.created = datetime.now()
        self.modified = datetime.now()
        super(App, self).save()

        
class Chain(models.Model):
    app = models.OneToOneField(App, related_name='chain')
    services = models.TextField(default="")
