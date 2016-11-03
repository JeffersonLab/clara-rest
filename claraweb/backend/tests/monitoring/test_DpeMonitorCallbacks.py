#!/usr/bin/env python
# coding=utf-8

import datetime
import json
import unittest

import mock
from claraweb.backend.rest.Container.models import Container
from claraweb.backend.rest.DPE.models import DPE
from xmsg.core.xMsgMessage import xMsgMessage

from claraweb.backend.rest.Service.models import ServiceEngine

date = datetime.datetime(2015, 9, 24, 14, 9, 12, 647427)

reg_msg = {
  "DPERegistration": {
    "hostname": "1.1.1.1",
    "language": "java",
    "n_cores": 8,
    "memory_size": 64,
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
        nodes = DPE.objects.count()
        containers = Container.objects.count()
        services = ServiceEngine.objects.count()
        if nodes and containers and services:
            return True
        else:
            return False

    def make_serialized_msg(self, test_case):
        return xMsgMessage.from_string("topic", json.dumps(test_case))

    @mock.patch('claraweb.backend.monitoring.DpeMonitorCallBacks.DpeMonitorCallBack')
    def test_register_dpe_first_time_should_register_dpe_in_db(self, dpe_monitor):
        dpe_monitor.save_runtime_data.return_value = ""
        serialized_msg = self.make_serialized_msg(reg_msg)
        dpe_monitor.callback(serialized_msg)
        dpe_monitor.callback.assert_called_with(serialized_msg)


if __name__ == "__main__":
    unittest.main()
