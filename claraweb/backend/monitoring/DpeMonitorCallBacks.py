# coding=utf-8

from influxdb import InfluxDBClient
from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.core.xMsgUtil import xMsgUtil

from clara.base.ClaraUtils import ClaraUtils
from claraweb.rest.DPE.models import DPE
from claraweb.rest.Container.models import Container
from claraweb.rest.Service.models import ServiceEngine
from claraweb.backend.monitoring.MsgHelpers import RuntimeMsgHelper, RegistrationMsgHelper


class DpeMonitorCallBack(xMsgCallBack):
    """ Callback function for the REST server monitoring subscription
    """

    def callback(self, msg):
        """DPE Monitor Callback, receives xMsgMessage with DPE data.

        Args:
            msg (xMsgMessage): Message containing the DPE runtime/reg. data
        """
        save_runtime_data(msg)
        save_registration_data(msg)
        return msg


def save_runtime_data(msg):
    """Stores the DPE's runtime information for the time series based DPE

    Args:
        msg (xMsgMessage): Message containing the DPE runtime data
    """
    run_data = RuntimeMsgHelper(msg)
    reg_data = RegistrationMsgHelper(msg)

    client = InfluxDBClient(database="claraRuntime")
    dpe = run_data.get_dpe()
    points = [
        {
            'measurement': 'dpe_runtime',
            'fields': {
                'cpu_usage': float(dpe['cpu_usage']),
                'mem_usage': dpe['memory_usage'],
                'load': float(dpe['load']),
            }
        }
    ]
    print run_data.get_dpe()['cpu_usage']

    tags = {
            'host': reg_data.get_dpe()['hostname'],
            'language': reg_data.get_dpe()['language'],
        }
    client.write_points(points=points, tags=tags)

    for service in run_data.get_services():
        points = [
            {
                'measurement': 'service_runtime',
                'fields': {
                    'bytes_sent': service['bytes_sent'],
                    'bytes_recv': service['bytes_recv'],
                    'n_requests': service['n_requests'],
                    'n_failures': service['n_failures'],
                }
            }
        ]
        tags = {
            'service': service['name'],
        }
        client.write_points(points=points, tags=tags)

    xMsgUtil.log("[%s]: Entry created for Runtime..." % run_data.get_dpe()['hostname'])


def save_registration_data(msg):
    """Stores the DPE's registration information for the time series based DPE

    Args:
        msg (xMsgMessage): Message containing the DPE runtime data
    """
    reg_data = RegistrationMsgHelper(msg)
    dpe = reg_data.get_dpe()
    dpe['start_time'] = dpe['start_time'].replace("/", "-")
    containers = dpe.pop('containers')
    node, _ = DPE.objects.get_or_create(defaults={'hostname': dpe['hostname']},
                                        **dpe)
    node.save()

    for cr in containers:
        cr['start_time'] = cr['start_time'].replace("/", "-")
        if ClaraUtils.is_container_name(cr['name']):
            cr['name'] = ClaraUtils.get_container_name(cr['name'])

        container, _ = Container.objects.get_or_create(dpe=node,
                                                       author=cr['author'],
                                                       name=cr['name'],
                                                       start_time=cr['start_time'])
        container.save()
        services = cr.pop('services')

        for sr in services:
            sr['start_time'] = sr['start_time'].replace("/", "-")
            service, _ = ServiceEngine.objects.get_or_create(container=container,
                                                             class_name=sr['class_name'],
                                                             engine_name=sr['engine_name'],
                                                             author=sr['author'],
                                                             version=sr['version'],
                                                             description=sr['description'],
                                                             start_time=sr['start_time'])
            service.save()

        xMsgUtil.log("[%s]: Database entry created (Registration)..." % str(node))
