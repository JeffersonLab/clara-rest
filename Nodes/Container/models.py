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

from claraweb.orchestrators.orchestrator import WebOrchestrator
from claraweb.utils.Validators import validate_node_existence
from Nodes.models import Node


class Container(models.Model):
    container_id = models.AutoField(primary_key=True, null=False)
    dpe = models.ForeignKey(Node, related_name='containers',
                            validators=[validate_node_existence])
    name = models.CharField(blank=False, max_length=20)
    created = models.DateTimeField(null=True)
    language = models.CharField(blank=False, max_length=20)
    modified = models.DateTimeField(null=True)

    def __str__(self):
        return "%s:%s" % (str(self.dpe.canonical_name),str(self.name))

    def save(self):
        if self.created is None:
            self.created = datetime.now()

        self.modified = datetime.now()
        super(Container, self).save()

        try:
            orchestrator = WebOrchestrator()
            orchestrator.deploy_container(str(self))

        except Exception as e:
            self.delete()
            raise Exception("Could not create container: %s" % e)

    def delete(self):
        try:
            orchestrator = WebOrchestrator()
            orchestrator.remove_container(str(self))

        except Exception as e:
            raise Exception(e)
            return

        super(Container, self).delete()

    class Meta:
        ordering = ('created',)
