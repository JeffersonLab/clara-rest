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

from claraweb.utils.CWConstants import CLARA_SUPPORTED_LANGUAGES


class Node(models.Model):
    node_id = models.AutoField(primary_key=True)
    hostname = models.GenericIPAddressField(blank=False)
    canonical_name = models.CharField(blank=False, max_length=40)
    language = models.CharField(blank=False,
                                max_length=20,
                                choices=CLARA_SUPPORTED_LANGUAGES)
    n_cores = models.IntegerField(blank=False)
    memory_size = models.CharField(blank=False, max_length=20)
    created = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)

    class Meta:
        ordering = ('hostname',)

    def save(self):
        if self.created is None:
            self.created = datetime.now()
            self.canonical_name = "%s:%s" % (str(self.hostname), self.language)
        self.modified = datetime.now()
        super(Node, self).save()

    def __str__(self):
        return str(self.canonical_name)

    def __int__(self):
        return int(self.node_id)
