# coding=utf-8

import json


class RuntimeMsgHelper(object):
    """Parser helper class for Clara web application

    Attributes:
        message (xMsgMessage): Dpe Runtime data message
            information for specific DPE
    """
    def __init__(self, msg):
        self._message = msg.data

    def __str__(self):
        """Returns the runtime message (JSON) in string format

        Returns:
            message (String): message as a python string
        """
        return str(self._message)

    def get_dpe(self):
        """Gets the dpe runtime information in JSON format

        It will return:

        * the DPE info
        * Containers registered and running in this DPE
        * Services registered and running in this DPE

        Returns:
            DPE_Registration (JSON object)
        """
        return json.loads(self._message)['DPERuntime']

    def get_containers(self):
        """Returns the containers registered in DPE and its runtime data

        Returns:
            containers (Array): array with the containers runtime data
        """
        dpe_runtime = json.loads(self._message)['DPERuntime']
        if 'containers' in dpe_runtime:
            return dpe_runtime['containers']
        return []

    def get_services(self):
        """Returns the services runtime data

        Returns:
            service_array (Array): array with the services runtime data
        """
        service_array = []
        for container in self.get_containers():
            if 'services' in container:
                for service in container['services']:
                    service_array.append(service)
        return service_array

    def to_JSON(self):
        return json.loads(self._message)


class RegistrationMsgHelper(object):
    """Parser helper class for Clara web application

    Attributes:
        message (String): serialized string message(JSON) with the registration
            information for specific DPE
    """
    def __init__(self, msg):
        self._message = msg.data

    def __str__(self):
        """Returns the registration message (JSON) in string format

        Returns:
            message (String): message as a python string
        """
        return str(self._message)

    def get_dpe(self):
        """Gets the dpe registration data in JSON format

        It will return:

        * the DPE info
        * Containers registered and running in this DPE
        * Services registered and running in this DPE

        Returns:
            DPE_Registration (JSON object)
        """
        return json.loads(self._message)['DPERegistration']

    def get_containers(self):
        """Returns the containers registered in DPE

        Returns:
            containers (Array): array with the containers information
        """
        dpe_registration = json.loads(self._message)['DPERegistration']
        if 'containers' in dpe_registration:
            return dpe_registration['containers']
        return []

    def get_services(self):
        """Returns the services registered in DPE

        Returns:
            service_array (Array): array with the services information
        """
        service_array = []
        for container in self.get_containers():
            if 'services' in container['ContainerRegistration']:
                for service in container['ContainerRegistration']['services']:
                    service_array.append(service)
        return service_array
