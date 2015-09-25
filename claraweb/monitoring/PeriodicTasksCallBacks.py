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

from claraweb.monitoring.RegMsgHelper import RegMsgHelper
from Nodes.Container.Service.models import ServiceEngine
from Nodes.Container.models import Container
from Nodes.models import Node


class RegistrationSubscriberDataCallBack(xMsgCallBack):

    def callback(self, msg):
        reg_msg = RegMsgHelper(msg.get_data())
        dpe_data = reg_msg.get_dpe_data()
        containers = dpe_data.pop('containers')

        node, created = Node.objects.get_or_create(dpe_data)
        node.save()

        for reg_container in containers:
            filtered_container = reg_container['ContainerRegistration']
            services = filtered_container.pop('services')
            container, created = Container.objects.get_or_create(dpe=node,
                                                                 author=filtered_container['author'],
                                                                 name=filtered_container['name'],
                                                                 language=filtered_container['language'],
                                                                 start_time=filtered_container['start_time'])
            container.save()

            for reg_service in services:
                filtered_service = reg_service['ServiceRegistration']
                service, created = ServiceEngine.objects.get_or_create(container=container,
                                                                       class_name=filtered_service['class_name'],
                                                                       engine_name=filtered_service['engine_name'],
                                                                       author=filtered_service['author'],
                                                                       version=filtered_service['version'],
                                                                       language=filtered_service['language'],
                                                                       description=filtered_service['description'],
                                                                       start_time=filtered_service['start_time'])
                service.save()


class RuntimeSubscriberDataCallBack(xMsgCallBack):

    def callback(self, msg):
        pass
