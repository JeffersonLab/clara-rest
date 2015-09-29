#
# Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its
# documentation for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement.
#
# Author Ricardo Oyarzun
# Department of Experimental Nuclear Physics, Jefferson Lab.
#
# IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
# INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
# THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
#
# JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
# HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
# SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#

from django.db import models
from datetime import datetime


class Node(models.Model):
    node_id = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=40, blank=False)
    language = models.CharField(blank=False, max_length=20)
    n_cores = models.IntegerField(blank=False)
    memory_size = models.CharField(blank=False, max_length=20)

    start_time = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)

    def __str__(self):
        return "%s_%s" % (self.hostname, self.language)

    def __int__(self):
        return int(self.node_id)

    def save(self, *args, **kwargs):
        if self.start_time:
            self.modified = datetime.now()
        else:
            self.start_time = datetime.now()
            self.modified = datetime.now()
        super(Node, self).save(*args, **kwargs)
