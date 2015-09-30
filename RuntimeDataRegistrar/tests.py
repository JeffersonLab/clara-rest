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
from datetime import datetime
import simplejson as json
from django.test import TestCase
from models import DPESnapshot
from claraweb.monitoring.DpeMonitorCallBacks import RunDataCallBack
from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.data import xMsgData_pb2

TEST_CASE = {
  "DPERuntime": {
    "host": "192.168.1.1",
    "snapshot_time": str(datetime.now()),
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
                }
              }
            ]
          }
      }
    ]
  }
}

class DpeSnapshotTests(TestCase):
    
    def setUp(self):
        TestCase.setUp(self)
        
    def test_create_a_simple_snapshot_from_test_case(self):
        snap = DPESnapshot.builder(TEST_CASE)
        snap.save()
        self.assertIsInstance(snap, DPESnapshot)

    def test_insertion_into_db(self):
        DPESnapshot.builder(TEST_CASE).save()
        self.assertEqual(1, len(DPESnapshot.objects.all()))

    def test_creation_from_rundatacallback(self):
        data = xMsgData_pb2.xMsgData()
        data.STRING = bytes(json.dumps(TEST_CASE))
        msg = xMsgMessage.create_with_xmsg_data("topic", data)
        result = RunDataCallBack().callback(msg)
        self.assertEqual(1, len(DPESnapshot.objects.all()))
        self.assertTrue("DPERuntime" in DPESnapshot.objects.all()[0].get_data())
