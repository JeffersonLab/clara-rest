# coding=utf-8

from clara.DPE.models import Node
from clara.Service.models import ServiceEngine
from clara.base.ClaraUtils import ClaraUtils
from influxdb import InfluxDBClient
from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.core.xMsgUtil import xMsgUtil

from clara.rest.Container import Container
from clara.web_backend.monitoring.MsgHelpers import RuntimeMsgHelper, RegistrationMsgHelper


class DpeMonitorCallBack(xMsgCallBack):

    def callback(self, msg):
        save_runtime_data(msg)
        save_registration_data(msg)


def save_runtime_data(msg):
    run_data = RuntimeMsgHelper(msg)
    reg_data = RegistrationMsgHelper(msg)

    client = InfluxDBClient(database="claraRuntime")

    points = [
        {
            'measurement': 'dpe_runtime',
            'fields': {
                'cpu_usage': run_data.get_dpe()['cpu_usage'],
                'mem_usage': run_data.get_dpe()['memory_usage'],
                'load': run_data.get_dpe()['load'],
            }
        }
    ]

    tags = {
            'host': reg_data.get_dpe()['hostname'],
            'language': reg_data.get_dpe()['language'],
        }
    client.write_points(points=points, tags=tags)
    xMsgUtil.log("[%s]: Entry created for Runtime..." % run_data.get_dpe()['hostname'])


def save_registration_data(msg):
    reg_data = RegistrationMsgHelper(msg)
    dpe = reg_data.get_dpe()
    dpe['start_time'] = dpe['start_time'].replace("/", "-")
    containers = dpe.pop('containers')
    node, _ = Node.objects.get_or_create(defaults={'hostname': dpe['hostname']},
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
