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

import unittest
import json
import datetime
from xmsg.data import xMsgData_pb2
from xmsg.core.xMsgMessage import xMsgMessage

from ClaraWebREST.monitoring.DpeMonitorCallBacks import DpeMonitorCallBack
from ClaraNodes.Container.Service.models import ServiceEngine
from ClaraNodes.Container.models import Container
from ClaraNodes.models import Node

date = datetime.datetime(2015, 9, 24, 14, 9, 12, 647427)

reg_msg = {
  "DPERegistration": {
    "hostname": "1.1.1.1",
    "language": "java",
    "n_cores": 8,
    "memory_size": "64M",
    "start_time": str(date),
    "containers": [
      {
        'ContainerRegistration': {
          "name": "1.1.1.1:SomeContainerName",
          "language": "_java",
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
                "language": "Java",
                "start_time": str(date)
              }
            }
          ]
        }
      }
    ]
  },
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
  }
}


class TestMonitorCallbacks(unittest.TestCase):

    def check_in_db(self):
        nodes = Node.objects.count()
        containers = Container.objects.count()
        services = ServiceEngine.objects.count()
        if nodes and containers and services:
            return True
        else:
            return False

    def make_serialized_msg(self, test_case):
        data = xMsgData_pb2.xMsgData()
        data.STRING = json.dumps(test_case)
        return xMsgMessage("topic", data.SerializeToString())

    def test_register_dpe_first_time_should_register_dpe_in_db(self):
        DpeMonitorCallBack().callback(self.make_serialized_msg(reg_msg))
        self.assertTrue(self.check_in_db())


if __name__ == "__main__":
    unittest.main()
