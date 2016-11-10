# coding=utf-8

import random
from clara.base.ClaraBase import ClaraBase
from xmsg.core.xMsgMessage import xMsgMessage


class MinimalOrchestrator(object):

    def __init__(self, host, port):
        self.name = self._generate_name()
        self.base = ClaraBase(self.name, host, port, host, port + 4)

    @staticmethod
    def _generate_name():
        return "orchestrator_%d" % (random.randint(0, 1000))

    def deploy_container(self, container):
        """Sends message to DPE requesting ti deploy container """

        topic = ":".join(["dpe", container.get_dpe_name()])
        data = "?".join(["startContainer", container.name, "2", "N/A"])
        self.base.send(xMsgMessage.from_string(topic=str(topic),
                                               data_string=str(data)))

    def remove_container(self, container):
        """Sends message to DPE requesting to stop container """
        topic = ":".join(["dpe", container.get_dpe_name()])
        data = "?".join(["stopContainer", container.name])
        self.base.send(xMsgMessage.from_string(topic=str(topic),
                                               data_string=str(data)))

    def deploy_service(self, service):
        """Sends message to DPE requesting to deploy service """
        topic = ":".join(["dpe", service.get_dpe_name()])
        data = "?".join(["startService", service.container.name,
                         service.engine_name, service.class_name, 2,
                         service.description, ""])
        self.base.send(xMsgMessage.from_string(topic=str(topic),
                                               data_string=str(data)))

    def remove_service(self, service):
        """Sends message to DPE requesting to stop Service"""
        topic = ":".join(["dpe", service.get_dpe_name()])
        data = "?".join(["stopService", service.container.name,
                         service.engine_name])
        self.base.send(xMsgMessage.from_string(topic=str(topic),
                                               data_string=str(data)))
