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
from xmsg.data.xMsgData_pb2 import xMsgData
from ClaraWebREST.monitoring.MsgHelpers import RegistrationMsgHelper
from xmsg.core.xMsgMessage import xMsgMessage

# DPE with no containers
TEST_CASE_1 = {
  "DPERegistration": {
    "language": "Java",
    "start_time": "10:10:10",
    "n_cores": 8,
    "host": "somecontainername",
    "memory_size": "64M",
    "n_containers": 1,
    "containers": []
  }
}

# DPE with one containers, no services
TEST_CASE_2 = {
  "DPERegistration": {
    "language": "Java",
    "start_time": "10:10:10",
    "n_cores": 8,
    "host": "somecontainername",
    "memory_size": "64M",
    "n_containers": 1,
    "containers": [
      {
        "ContainerRegistration": {
          "name": "ContainerName",
          "language": "Java",
          "author": "Vardan",
          "startTime": "10:10:10",
          "nServices": 0,
          "services": []
        }
      }
    ]
  }
}

# DPE with one containers, and some services
TEST_CASE_3 = {
  "DPERegistration": {
    "language": "Java",
    "start_time": "10:10:10",
    "n_cores": 8,
    "host": "somecontainername",
    "memory_size": "64M",
    "n_containers": 2,
    "containers": [
      {
        "ContainerRegistration": {
          "name": "SomeContainerName1",
          "language": "Java",
          "author": "Vardan",
          "startTime": "10:10:10",
          "nServices": 2,
          "services": [
            {
              "ServiceRegistration": {
                "className": "SomeClassName",
                "engineName": "SomeEngineName",
                "author": "Vardan",
                "version": "1.0",
                "description": "what i do",
                "language": "Java",
                "startTime": "10:10:10"
              }
            },
            {
              "ServiceRegistration": {
                "className": "SomeClassName",
                "engineName": "SomeEngineName",
                "author": "Vardan",
                "version": "1.0",
                "description": "what i do",
                "language": "Java",
                "startTime": "10:10:10"
              }
            }
          ]
        }
      }
    ]
  }
}

# DPE with 2 containers, no services
TEST_CASE_4 = {
  "DPERegistration": {
    "language": "Java",
    "start_time": "10:10:10",
    "n_cores": 8,
    "host": "somecontainername",
    "memory_size": "64M",
    "n_containers": 2,
    "containers": [
      {
        "ContainerRegistration": {
          "name": "SomeContainerName1",
          "language": "Java",
          "author": "Vardan",
          "startTime": "10:10:10",
          "nServices": 0,
          "services": []
        }
      },
      {
        "ContainerRegistration": {
          "name": "SomeContainerName2",
          "language": "Java",
          "author": "Vardan",
          "startTime": "10:10:10",
          "nServices": 0,
          "services": []
        }
      }
    ]
  }
}
# DPE with 2 containers, one container with one service
TEST_CASE_5 = {
  "DPERegistration": {
    "language": "Java",
    "start_time": "10:10:10",
    "n_cores": 8,
    "host": "somecontainername",
    "memory_size": "64M",
    "n_containers": 2,
    "containers": [
      {
        "ContainerRegistration": {
          "name": "SomeContainerName",
          "language": "Java",
          "author": "Vardan",
          "startTime": "10:10:10",
          "nServices": 1,
          "services": [
            {
              "ServiceRegistration": {
                "className": "SomeClassName",
                "engineName": "SomeEngineName",
                "author": "Vardan",
                "version": "1.0",
                "description": "description of what i do",
                "language": "Java",
                "startTime": "10:10:10"
              }
            }
          ]
        }
      },
      {
        "ContainerRegistration": {
          "name": "SomeContainerName",
          "language": "Java",
          "author": "Vardan",
          "startTime": "10:10:10",
          "nServices": 0,
          "services": []
        }
      }
    ]
  }
}


class TestRegistrationMsgHelper(unittest.TestCase):

    def make_serialized_msg(self, case):
        return xMsgMessage.create_with_string("topic", json.dumps(case))

    def test_convert_message_to_json(self):
        parser = RegistrationMsgHelper(self.make_serialized_msg(TEST_CASE_1))
        self.assertTrue("DPERegistration" in str(parser))

    def test_get_containers(self):
        parser = RegistrationMsgHelper(self.make_serialized_msg(TEST_CASE_2))
        self.assertFalse("DPERegistration" in parser.get_containers())
        self.assertIsNotNone(parser.get_containers())
        parser = RegistrationMsgHelper(self.make_serialized_msg(TEST_CASE_4))
        self.assertEqual(len(parser.get_containers()), 2)

    def test_message_with_empty_containers_returns_empty_array(self):
        parser = RegistrationMsgHelper(self.make_serialized_msg(TEST_CASE_1))
        self.assertEqual([], parser.get_containers())

    def test_get_the_two_services_in_container(self):
        parser = RegistrationMsgHelper(self.make_serialized_msg(TEST_CASE_3))
        self.assertEqual(len(parser.get_services()), 2)

    def test_get_no_services_in_container(self):
        parser = RegistrationMsgHelper(self.make_serialized_msg(TEST_CASE_2))
        self.assertEqual(len(parser.get_services()), 0)
        self.assertEqual([], parser.get_services())

    def test_get_the_one_service_in_dpe_with_two_containers_one_empty(self):
        parser = RegistrationMsgHelper(self.make_serialized_msg(TEST_CASE_5))
        self.assertEqual(len(parser.get_services()), 1)


if __name__ == "__main__":
    unittest.main()
