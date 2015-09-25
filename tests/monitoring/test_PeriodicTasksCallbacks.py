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

import unittest
import json
import datetime
from xmsg.data import xMsgData_pb2
from xmsg.core.xMsgMessage import xMsgMessage

from claraweb.monitoring.PeriodicTasksCallBacks import RegistrationSubscriberDataCallBack
from Nodes.Container.Service.models import ServiceEngine
from Nodes.Container.models import Container
from Nodes.models import Node

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
        "ContainerRegistration": {
          "name": "1.1.1.1:SomeContainerName",
          "language": "_java",
          "author": "Vardan",
          "start_time": str(date),
          "services": [
            {
              "ServiceRegistration": {
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
  }
}


class TestPeriodicTasksCallbacks(unittest.TestCase):

    def setUp(self):
        self.reg_callback = RegistrationSubscriberDataCallBack()

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
        self.reg_callback.callback(self.make_serialized_msg(reg_msg))
        self.assertTrue(self.check_in_db())

    def test_register_dpe_second_time_should_not_save_but_should_register_modification(self):
        pass

if __name__ == "__main__":
    unittest.main()