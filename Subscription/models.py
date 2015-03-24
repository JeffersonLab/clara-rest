'''
Created on 24-03-2015

@author: royarzun
'''
from django.db import models


class SubscriptionHandler(models.Model):
    INFO = 'INFO'
    WARNING ='WARNING'
    ERROR = 'ERROR'
    DATA = 'DATA'
    DONE = 'DONE'
    MESSAGE_TYPE = (
        (INFO, 'INFO'),
        (WARNING, 'WARNING'),
        (ERROR, 'ERROR'),
        (DATA, 'DATA'),
        (DONE, 'DONE')
    )
    subscription_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=10,choices=MESSAGE_TYPE,
                            default=INFO)
    created = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)
    
    def __str__(self):
        return  str(self.type)+":"+str(self.subscription_id)
    
    def save(self):
        if self.created is None:
            self.created = datetime.now()
        self.modified = datetime.now()
        super(SubscriptionHandler, self).save()
