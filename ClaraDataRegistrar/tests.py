#!/usr/bin/env python
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

import simplejson as json
from datetime import datetime
from django.test import TestCase
from xmsg.core.xMsgMessage import xMsgMessage

from ClaraWebREST.monitoring.DpeMonitorCallBacks import DpeMonitorCallBack
from ClaraDataRegistrar.models import DPESnapshot


date = datetime.now()
TEST_CASE = {
  "DPERuntime": {
    "hostname": "192.168.1.1",
    "snapshot_time": str(date),
    "cpu_usage": 760,
    "memory_usage": 63,
    "load": 0.9,
    "containers": [
      {
        "ContainerRuntime": {
          "name": "192.168.1.1:cont_name",
          "snapshot_time": 11245590398,
          "n_requests": 1000,
          "services": [
            {
              "ServiceRuntime": {
                "name": "192.168.1.1:cont_name:S1",
                "snapshot_time": 1954869020,
                "n_requests": 1000,
                "n_failures": 10,
                "shm_reads": 1000,
                "shm_writes": 1000,
                "bytes_recv": 0,
                "bytes_sent": 0,
                "exec_time": 134235243543
              },
            },
          ]
        }
      }
    ]
  },
  "DPERegistration": {
    "hostname": "1.1.1.1",
    "language": "java",
    "n_cores": 8,
    "memory_size": 64000000,
    "start_time": str(date),
    "containers": [
      {
        'ContainerRegistration': {
          "name": "1.1.1.1:SomeContainerName",
          "author": "Vardan",
          "start_time": str(date),
          "services": [
            {
              'ServiceRegistration': {
                "class_name": "SomeClassName",
                "engine_name": "SomeEngineName",
                "author": "Vardan",
                "version": "1.0",
                "description": "description of what i do",
                "start_time": str(date)
              }
            }
          ]
        }
      }
    ]
  },
}


class DpeSnapshotTests(TestCase):

    def make_serialized_msg(self):
        return xMsgMessage.create_with_string("topic", json.dumps(TEST_CASE))

    def test_create_a_simple_snapshot_from_test_case(self):
        snap = DPESnapshot.builder(TEST_CASE)
        snap.save()
        self.assertIsInstance(snap, DPESnapshot)

    def test_insertion_into_db(self):
        DPESnapshot.builder(TEST_CASE).save()
        self.assertEqual(1, len(DPESnapshot.objects.all()))

    def test_creation_from_rundatacallback(self):
        DpeMonitorCallBack().callback(self.make_serialized_msg())
        self.assertEqual(1, len(DPESnapshot.objects.all()))
        self.assertTrue("DPERuntime" in DPESnapshot.objects.all()[0].get_data())
