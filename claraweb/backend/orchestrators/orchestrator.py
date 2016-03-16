# coding=utf-8

from xmsg.core.xMsgMessage import xMsgMessage

from clara.base.ClaraBase import ClaraBase
from clara.base.ClaraUtils import ClaraUtils
from clara.util.CConstants import CConstants


class RESTOrchestrator(ClaraBase):
    """Web orchestrator wrapper: this class will be in charge of connecting
    the database with Clara's registrar information
    """
    def __init__(self):
        super(RESTOrchestrator, self).__init__(name="clara_rest_server",
                                               proxy_host="localhost",
                                               frontend_host="localhost",
                                               proxy_port=7771,
                                               frontend_port=8888)
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
