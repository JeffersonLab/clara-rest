#
# Copyright (C) 2015. Jefferson Lab, Clara framework (JLAB). All Rights Reserved.
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

from ClaraWebREST.orchestrators.orchestrator import RESTOrchestrator
from ClaraWebREST.utils.Validators import validate_node_existence
from clara.models import Node


class Container(models.Model):
    container_id = models.AutoField(primary_key=True, null=False)
    dpe = models.ForeignKey(Node, related_name='containers',
                            validators=[validate_node_existence])
    author = models.CharField(blank=False, max_length=40)
    name = models.CharField(blank=False, max_length=40)

    start_time = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)

    class Meta:
        unique_together = ('dpe', 'name')

    def __str__(self):
        return self.get_canonical_name()

    def get_dpe_name(self):
        return str(self.dpe)

    def get_language(self):
        return str(self.dpe.language)

    def get_canonical_name(self):
        return str(self.get_dpe_name() + ":" + self.name)

    def save(self, *args, **kwargs):
        orchestrator = RESTOrchestrator()
        orchestrator.deploy_container(self.get_dpe_name(), self.name)
        super(Container, self).save(*args, **kwargs)
