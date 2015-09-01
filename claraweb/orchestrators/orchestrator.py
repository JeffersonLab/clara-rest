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

from xmsg.core.xMsgMessage import xMsgMessage

from clara.base.ClaraUtils import ClaraUtils
from clara.base.CConstants import CConstants
from clara.base.CBase import CBase


class WebOrchestrator:
    """Web orchestrator wrapper: this class will be in charge of connecting
    the database with Clara's registrar information
    """
    def __init__(self):
        self.base = CBase("localhost")

    def __build_data(self, *args):
        """Data builder method

        Returns a string with the form:
        data?data1?data...
        Args:
            args: Non keyworded argument list

        Returns:
            data (String): data string
        """
        return str(CConstants.DATA_SEP).join(args)

    def __build_topic(self, *args):
        """Topic builder method

        Returns a string with the form:
        data:data1:data...
        Args:
            args: Non keyworded argument list

        Returns:
            topic (String): topic string
        """
        return str(CConstants.TOPIC_SEP).join(args)

    def __build_message(self, topic, data=None):
        """Message builder
        Args:
            topic (String): topic for the message
            data (String): data string for the message
        Returns
            xMsgMessage: message built
        """
        return xMsgMessage(topic, data)

    def __send_message(self, message):
        """Sends message to specific Clara Actor

        Args:
            message (xMsgMessage): message for the orchestrator, to be sent
                to the specific actor. Message has the following structure:
                * topic: ACTOR_LABEL_IDENTIFIER (DPE, CONTAINER, SERVICE)
                * data: action to be performed by xMsg actor
        """
        message.get_metadata().dataType="text/string"
        try:
            self.base.generic_send(message)
        except Exception as e:
            raise Exception("Could not send request: %s" % e)

    def dpe_exit(self, dpe_name):
        """Forces dpe to exit

        The method will send an exit action message to an specific DPE

        Args:
            dpe_name (String): dpe name
        """
        topic = self.__build_topic(CConstants.DPE, dpe_name)
        msg = self.__build_message(topic, CConstants.DPE_EXIT)
        self.__send_message(msg)

    def dpe_ping(self, dpe_name):
        """Simple ping function to check if dpe is active or not

        Args:
            dpe_name (String): the canonical name of the DPE

        Returns:
            boolean: True if active otherwise False
        """
        # For now it will return False and will not do anything
        # Just a placeholder
        return False

    def deploy_container(self, container_name):
        """Sends a request to deploy a container and waits until it is deployed.
        The request is sent to a running DPE of the given language.
        If no DPE is running in the node, the message is lost.
        If there is a container with the given name in the DPE, the request is
        ignored.

        Args:
            container_name (String): the canonical name of the container
        """
        host = ClaraUtils.get_hostname(container_name)
        dpe = ClaraUtils.get_dpe_name(container_name)
        name = ClaraUtils.get_container_name(container_name)

        topic = self.__build_topic(CConstants.DPE, dpe)
        data = self.__build_data(CConstants.START_CONTAINER, name)

        msg = self.__build_message(topic, data)
        self.__send_message(msg)

    def remove_container(self, container_name):
        """Sends a request to remove a container.
        The request is sent to a running DPE of the given language.
        If no DPE is running in the node, the message is lost.
        If there is no container of the given name in the DPE, the request is
        ignored.

        Args:
            container_name (String): the canonical name of the container
        """
        host = ClaraUtils.get_hostname(container_name)
        dpe = ClaraUtils.get_dpe_name(container_name)
        name = ClaraUtils.get_container_name(container_name)

        topic = self.__build_topic(CConstants.DPE, dpe)
        data = self.__build_data(CConstants.REMOVE_CONTAINER, name)

        msg = self.__build_message(topic, data)
        self.__send_message(msg)
