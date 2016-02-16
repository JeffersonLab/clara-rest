#!/usr/bin/env python
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

from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.core.xMsgUtil import xMsgUtil

from ClaraDataRegistrar.models import DPESnapshot
from ClaraWebREST.monitoring.MsgHelpers import RuntimeMsgHelper, RegistrationMsgHelper
from ClaraNodes.Container.Service.models import ServiceEngine
from ClaraNodes.Container.models import Container
from ClaraNodes.models import Node


class DpeMonitorCallBack(xMsgCallBack):

    def callback(self, msg):
        save_runtime_data(msg)
        save_registration_data(msg)


def save_runtime_data(msg):
    run_data = RuntimeMsgHelper(msg)
    dpe = DPESnapshot.builder(run_data.to_JSON())
    dpe.save()
    xMsgUtil.log("[%s]: Database entry created (Runtime)..." % dpe.name)


def save_registration_data(msg):
    reg_data = RegistrationMsgHelper(msg)
    dpe = reg_data.get_dpe()
    dpe['start_time'] = dpe['start_time'].replace("/", "-")
    containers = dpe.pop('containers')
    node, _ = Node.objects.get_or_create(defaults={'hostname': dpe['hostname']},
                                         **dpe)
    node.save()

    for cr in containers:
        cr = cr['ContainerRegistration']
        cr['start_time'] = cr['start_time'].replace("/", "-")
        container, _ = Container.objects.get_or_create(dpe=node,
                                                       author=cr['author'],
                                                       name=cr['name'],
                                                       start_time=cr['start_time'])
        container.save()
        services = cr.pop('services')

        for sr in services:
            sr = sr['ServiceRegistration']
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
