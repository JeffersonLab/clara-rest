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

from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.core.xMsgUtil import xMsgUtil

from ClaraWebREST.monitoring.RuntimeMsgHelper import RuntimeMsgHelper
from ClaraWebREST.monitoring.RegMsgHelper import RegMsgHelper
from RuntimeDataRegistrar.models import DPESnapshot
from Nodes.Container.Service.models import ServiceEngine
from Nodes.Container.models import Container
from Nodes.models import Node


class DpeMonitorCallBack(xMsgCallBack):

    def callback(self, msg):
        save_runtime_data(msg)
        save_registration_data(msg)


def save_runtime_data(msg):
    try:
        run_msg = RuntimeMsgHelper(msg.get_data())
        snap = DPESnapshot.builder(run_msg.get_json_object())
        snap.save()
        xMsgUtil.log("dpe@%s: Database entry created..." % snap.name)

    except Exception as e:
        print e
        xMsgUtil.log("Something went wrong saving runtime data...")


def save_registration_data(msg):
    try:
        reg_msg = RegMsgHelper(msg.get_data())
        dpe_data = reg_msg.get_dpe_data()
        containers = dpe_data.pop('containers')
        dpe_data['start_time'] = dpe_data['start_time'].replace("/", "-")
        node, created = Node.objects.get_or_create(defaults={'hostname': dpe_data['hostname']},
                                                   **dpe_data)

        node.save()

        if created:
            xMsgUtil.log("dpe@%s: Database entry created..." % dpe_data['hostname'])

        for reg_container in containers:
            cur_container = reg_container['ContainerRegistration']
            container, created = Container.objects.get_or_create(dpe=node,
                                                                 author=cur_container['author'],
                                                                 name=cur_container['name'],
                                                                 language=cur_container['language'],
                                                                 start_time=cur_container['start_time'].replace("/", "-"))
            container.save()

            for reg_service in cur_container.pop('services'):
                cur_service = reg_service['ServiceRegistration']
                service, created = ServiceEngine.objects.get_or_create(container=container,
                                                                       class_name=cur_service['class_name'],
                                                                       engine_name=cur_service['engine_name'],
                                                                       author=cur_service['author'],
                                                                       version=cur_service['version'],
                                                                       language=cur_service['language'],
                                                                       description=cur_service['description'],
                                                                       start_time=cur_service['start_time'].replace("/", "-"))
                service.save()
        xMsgUtil.log("Registration saved for node : %s" % str(node))

    except Exception as e:
        print e
        xMsgUtil.log("Something went wrong registration data...")
