from django.db import models
from xsys.xMsgNode import xMsgNode


class Node(models.Model):
    
    ip = models.IPAddressField()
        
    def new_node(self):
        node = xMsgNode()
        node.__init__()