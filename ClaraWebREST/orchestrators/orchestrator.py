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

from xmsg.core.xMsgMessage import xMsgMessage

from clara.base.ClaraUtils import ClaraUtils
from clara.base.ClaraBase import ClaraBase
from clara.util.CConstants import CConstants


class RESTOrchestrator(ClaraBase):
    """Web orchestrator wrapper: this class will be in charge of connecting
    the database with Clara's registrar information
    """
    def __init__(self):
        super(RESTOrchestrator, self).__init__(name="clara_rest_server",
                                               frontend="localhost",
                                               proxy_address="localhost")
        self.node_connection = self.connect()

    def __build_message(self, topic, data):
        return xMsgMessage.create_with_string(topic, data)


    def dpe_exit(self, dpe_name):
        """Forces dpe to exit

        The method will send an exit action message to an specific DPE

        Args:
            dpe_name (String): dpe name
        """
        topic = ClaraUtils.build_topic(CConstants.DPE, dpe_name)
        data = ClaraUtils.build_data(CConstants.DPE_EXIT)
        self.send(self.__build_message(topic, data))

    def deploy_container(self, dpe_name, container_name):
        """Sends a request to deploy a container and waits until it is deployed.
        The request is sent to a running DPE of the given language.
        If no DPE is running in the node, the message is lost.
        If there is a container with the given name in the DPE, the request is
        ignored.

        Args:
            dpe_name (String): the canonical name of dpe
            container_name (String): the canonical name of the container
        """
        topic = ClaraUtils.build_topic(CConstants.DPE, dpe_name)
        data = ClaraUtils.build_data(CConstants.START_CONTAINER, container_name)
        self.send(self.__build_message(topic, data))

    def remove_container(self, dpe_name, container_name):
        """Sends a request to remove a container.
        The request is sent to a running DPE of the given language.
        If no DPE is running in the node, the message is lost.
        If there is no container of the given name in the DPE, the request is
        ignored.

        Args:
            dpe_name (String): the canonical name of dpe
            container_name (String): the name of the container
        """
        topic = ClaraUtils.build_topic(CConstants.DPE, dpe_name)
        data = ClaraUtils.build_data(CConstants.REMOVE_CONTAINER, container_name)
        self.send(self.__build_message(topic, data))

    def deploy_service(self, container_name, engine_name, engine_class, pool_size):
        """Sends a request to deploy a service.
        The request is sent to a running container of the given language.
        If no container is running in the node, the message is lost.
        If there is no container of the given name in the DPE, the request is
        ignored.

        Args:
            container_name (String): the canonical name of the container
            engine_name (String): the name of the engine to deploy
            engine_class (String): the class that contains engine to deploy
            pool_size (int): Pool size for engine
        """
        topic = ClaraUtils.build_topic(CConstants.CONTAINER, container_name)
        data = ClaraUtils.build_data(CConstants.DEPLOY_SERVICE,
                                     engine_name, engine_class,
                                     pool_size)
        self.send(self.__build_message(topic, data))

    def remove_service(self, container_name, service_name):
        """Sends a request to remove a service.
        The request is sent to a running DPE of the given language.
        If no DPE is running in the node, the message is lost.
        If there is no container of the given name in the DPE, the request is
        ignored.

        Args:
            container_name (String): the canonical name of the container
            service_name (String): service name to remove
        """
        topic = ClaraUtils.build_topic(CConstants.CONTAINER, container_name)
        data = ClaraUtils.build_data(CConstants.REMOVE_SERVICE, service_name)
        self.send(self.__build_message(topic, data))
