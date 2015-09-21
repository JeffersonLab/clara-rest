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
import json
from xmsg.data import xMsgData_pb2


class RuntimeMsgHelper(object):
    """Parser helper class for Clara web application

    Attributes:
        message (String): serialized string message(JSON) with the runtime
            information for specific DPE
    """
    def __init__(self, message):
        ds_message = xMsgData_pb2.xMsgData()
        ds_message.ParseFromString(message)
        self.message = ds_message.STRING
        self.message_json = json.loads(ds_message.STRING)

    def __str__(self):
        """Returns the runtime message (JSON) in string format

        Returns:
            message (String): message as a python string
        """
        return str(self.message)

    def get_dpe_runtime_info(self):
        """Gets the dpe runtime information in JSON format

        It will return:

        * the DPE info
        * Containers registered and running in this DPE
        * Services registered and running in this DPE

        Returns:
            DPE_Registration (JSON object)
        """
        return self.message_json['DPERuntime']

    def get_containers(self):
        """Returns the containers registered in DPE and its runtime data

        Returns:
            containers (Array): array with the containers runtime data
        """
        return self.message_json['DPERuntime']['containers']

    def get_services(self):
        """Returns the services runtime data

        Returns:
            service_array (Array): array with the services runtime data
        """
        service_array = []
        for container in self.get_containers():
            for service in container['ContainerRuntime']['services']:
                service_array.append(service)
        return service_array

    def get_json_object(self):
        """Returns the runtime message in raw JSON

        Returns:
            message (JSON object): message as JSON object
        """
        return self.message_json
