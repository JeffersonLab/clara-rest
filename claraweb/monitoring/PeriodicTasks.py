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

from celery.schedules import crontab
from celery.task.base import periodic_task
from celery.utils.log import get_task_logger
from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgTopic import xMsgTopic

from claraweb.monitoring.PeriodicTasksCallBacks import *

logger = get_task_logger(__name__)


class RegistrationDataSubscriber(xMsg):
    
    def __init__(self):
        super(RegistrationDataSubscriber, self).__init__("RegistrationDataSubscriber",
                                                         "localhost",
                                                         "localhost")
        self.callback = RegistrationSubscriberDataCallBack()
        self.connection = self.connect(xMsgAddress(localhost))
        self.topic = xMsgTopic.wrap("RegistrationDataSubscriber")


class RuntimeDataSubscriber(xMsg):

    def __init__(self):
        super(RegistrationDataSubscriber, self).__init__("RuntimeDataSubscriber",
                                                         "localhost",
                                                         "localhost")
        self.callback = RuntimeSubscriberDataCallBack()
        self.connection = self.connect(xMsgAddress(localhost))
        self.topic = xMsgTopic.wrap("RuntimeDataSubscriber")


@periodic_task(run_every=(crontab()))
def pickup_registration_data_task():
    reg_subscriber = RegistrationDataSubscriber()
    counter = 0

    while counter < 30:
        reg_subscription = reg_subscriber.subscribe(self.connection,
                                                    self.topic,
                                                    self.callback)
        xMsgUtil.sleep(0.5)
        counter+=1
        
    reg_subscriber.unsubscribe(reg_subscription)
    reg_subscriber.destroy()
    logger.info("called: pickup_registration_data_task method...")


@periodic_task(run_every=(crontab()))
def pickup_runtime_data_task():
    run_subscriber = RuntimeDataSubscriber()
    counter = 0

    while counter < 30:
        run_subscription = run_subscriber.subscribe(self.connection,
                                                    self.topic,
                                                    self.callback)
        xMsgUtil.sleep(0.5)
        counter+=1

    run_subscriber.unsubscribe(run_subscription)
    run_subscriber.destroy()
    logger.info("called: pickup_runtime_data_task method...")


@periodic_task(run_every=(crontab()))
def periodic_cleandb_task():
    #  TODO: A periodic task to clean up the database.
    print "called: periodic_cleandb_task method..."
    logger.info("called: periodic_cleandb_task method...")
