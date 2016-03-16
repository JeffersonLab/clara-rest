#!/usr/bin/env python
# coding=utf-8

import unittest
import json
from xmsg.core.xMsgMessage import xMsgMessage
from claraweb.web_backend.monitoring.MsgHelpers import RuntimeMsgHelper


# DPE with no containers
TEST_CASE_1 = {
  "DPERuntime": {
    "host": "192.168.1.1",
    "snapshot_time": 112455111903,
    "cpu_usage": 760,
    "memory_usage": 63,
    "load": 0.9,
    "containers": [
    ]
  }
}

# DPE with one containers, no services
TEST_CASE_2 = {
  "DPERuntime": {
    "host": "192.168.1.1",
    "snapshot_time": 112455111903,
    "cpu_usage": 760,
    "memory_usage": 63,
    "load": 0.9,
    "containers": [
      {
         "ContainerRuntime": {
            "name": "192.168.1.1:SomeContainerName",
            "snapshot_time": 11245590398,
            "n_requests": 1000,
            "services": []
          }
      }
    ]
  }
}

# DPE with one containers, and some services
TEST_CASE_3 = {
  "DPERuntime": {
    "host": "192.168.1.1",
    "snapshot_time": 112455111903,
    "cpu_usage": 760,
    "memory_usage": 63,
    "load": 0.9,
    "containers": [
      {
         "ContainerRuntime": {
            "name": "192.168.1.1:SomeContainerName",
            "snapshot_time": 11245590398,
            "n_requests": 1000,
            "services": [
              {
                "ServiceRuntime": {
                  "name": "192.168.1.1:SomeContainerName:SomeServiceName0",
                  "snapshot_time": 1954869020,
                  "n_requests": 1000,
                  "n_failures": 10,
                  "shm_reads": 1000,
                  "shm_writes": 1000,
                  "bytes_recv": 0,
                  "bytes_sent": 0,
                  "exec_time": 134235243543
                }
              },
              {
                "ServiceRuntime": {
                  "name": "192.168.1.1:SomeContainerName:SomeServiceName1",
                  "snapshot_time": 1954869020,
                  "n_requests": 1000,
                  "n_failures": 10,
                  "shm_reads": 1000,
                  "shm_writes": 1000,
                  "bytes_recv": 0,
                  "bytes_sent": 0,
                  "exec_time": 134235243542
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
  "DPERuntime": {
    "host": "192.168.1.1",
    "snapshot_time": 112455111903,
    "cpu_usage": 760,
    "memory_usage": 63,
    "load": 0.9,
    "containers": [
      {
         "ContainerRuntime": {
            "name": "192.168.1.1:SomeContainerName0",
            "snapshot_time": 11245590398,
            "n_requests": 1000,
            "services": []
          }
      },
      {
         "ContainerRuntime": {
            "name": "192.168.1.1:SomeContainerName1",
            "snapshot_time": 11245590398,
            "n_requests": 1000,
            "services": []
          }
      }
    ]
  }
}

# DPE with 2 containers, one container with one service
TEST_CASE_5 = {
  "DPERuntime": {
    "host": "192.168.1.1",
    "snapshot_time": 112455111903,
    "cpu_usage": 760,
    "memory_usage": 63,
    "load": 0.9,
    "containers": [
      {
        "ContainerRuntime": {
          "name": "192.168.1.1:SomeContainerName0",
          "snapshot_time": 11245590398,
          "n_requests": 1000,
          "services": [
            {
              "ServiceRuntime": {
                "name": "192.168.1.1:SomeContainerName:SomeServiceName1",
                "snapshot_time": 1954869020,
                "n_requests": 1000,
                "n_failures": 10,
                "shm_reads": 1000,
                "shm_writes": 1000,
                "bytes_recv": 0,
                "bytes_sent": 0,
                "exec_time": 134235243542
              }
            }
          ]
        }
      },
      {
        "ContainerRuntime": {
          "name": "192.168.1.1:SomeContainerName1",
          "snapshot_time": 11245590398,
          "n_requests": 1000,
          "services": []
        }
      }
    ]
  }
}


class TestRuntimeMsgHelper(unittest.TestCase):

    def make_serialized_msg(self, case):
        return xMsgMessage.create_with_string("topic", json.dumps(case))

    def test_convert_message_to_json(self):
        parser = RuntimeMsgHelper(self.make_serialized_msg(TEST_CASE_1))
        self.assertTrue("DPERuntime" in str(parser))

    def test_get_containers(self):
        parser = RuntimeMsgHelper(self.make_serialized_msg(TEST_CASE_2))
        self.assertFalse("DPERuntime" in parser.get_containers())
        self.assertIsNotNone(parser.get_containers())
        parser = RuntimeMsgHelper(self.make_serialized_msg(TEST_CASE_4))
        self.assertEqual(len(parser.get_containers()), 2)

    def test_message_with_empty_containers_returns_empty_array(self):
        parser = RuntimeMsgHelper(self.make_serialized_msg(TEST_CASE_1))
        self.assertEqual([], parser.get_containers())

    def test_get_the_two_services_in_container(self):
        parser = RuntimeMsgHelper(self.make_serialized_msg(TEST_CASE_3))
        self.assertEqual(len(parser.get_services()), 2)

    def test_get_no_services_in_container(self):
        parser = RuntimeMsgHelper(self.make_serialized_msg(TEST_CASE_2))
        self.assertEqual(len(parser.get_services()), 0)
        self.assertEqual([], parser.get_services())

    def test_get_the_one_service_in_dpe_with_two_containers_one_empty(self):
        parser = RuntimeMsgHelper(self.make_serialized_msg(TEST_CASE_5))
        self.assertEqual(len(parser.get_services()), 1)


if __name__ == "__main__":
    unittest.main()
