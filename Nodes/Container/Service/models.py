#!/usr/bin/env python
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

from Nodes.Container.models import Container
"""
A CLARA service engine runs in one container at one DPE.<br>
Must be threadsafe. Must implement CLARA service engine interface.
"""


class ServiceEngine(models.Model):
    """
    A CLARA service engine runs in one container at one DPE.
    Must be threadsafe. Must implement CLARA service engine interface.
    """
    service_id = models.AutoField(primary_key=True)
    container = models.ForeignKey(Container, related_name='services')
    class_name = models.CharField(blank=False, max_length=40)
    engine_name = models.TextField(blank=True, default="")

    author = models.CharField(blank=False, max_length=40)
    version = models.CharField(blank=False, max_length=40)
    language = models.CharField(blank=False, max_length=40)
    description = models.CharField(blank=False, max_length=100)

    start_time = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)

    def __str__(self):
        return "%s:%s" % (str(self.container), self.engine_name)
