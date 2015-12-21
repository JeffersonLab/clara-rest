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
        dpe = DPESnapshot.builder(run_msg.get_json_object())
        dpe.save()
        xMsgUtil.log("dpe@%s: Database entry created..." % dpe.name)

    except Exception as e:
        print e
        xMsgUtil.log("Something went wrong saving runtime data...")


def save_registration_data(msg):
    try:
        reg_msg = RegMsgHelper(msg.get_data())
        dpe = reg_msg.get_dpe_data()

        dpe['start_time'] = dpe['start_time'].replace("/", "-")
        containers = dpe.pop('containers')
        node, _ = Node.objects.get_or_create(defaults={'hostname': dpe['hostname']},
                                             **dpe)

        node.save()

        for cr in containers:
            cr['start_time'] = cr['start_time'].replace("/", "-")
            container, _ = Container.objects.get_or_create(dpe=node,
                                                           author=cr['author'],
                                                           name=cr['name'],
                                                           language=cr['language'],
                                                           start_time=cr['start_time'])
            container.save()

            for sr in cr.pop('services'):
                sr['start_time'] = sr['start_time'].replace("/", "-")
                service, _ = ServiceEngine.objects.get_or_create(container=container,
                                                                 class_name=sr['class_name'],
                                                                 engine_name=sr['engine_name'],
                                                                 author=sr['author'],
                                                                 version=sr['version'],
                                                                 language=sr['language'],
                                                                 description=sr['description'],
                                                                 start_time=sr['start_time'])
                service.save()

        xMsgUtil.log("Registration saved for node : %s" % str(node))

    except Exception as e:
        print e
        xMsgUtil.log("Something went wrong registration data...")
