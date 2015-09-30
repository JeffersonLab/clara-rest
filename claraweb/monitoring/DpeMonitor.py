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
import os
import sys
import django
from argparse import ArgumentParser
from celery.utils.log import get_task_logger
from xmsg.core.xMsgUtil import xMsgUtil
proj_path = "/Users/royarzun/src/repo/naiads/clara-webapp/"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ClaraWebREST.settings")
sys.path.append(proj_path)
# This is so my local_settings.py gets loaded.
os.chdir(proj_path)
django.setup()
from claraweb.monitoring.base.PeriodicDataSubscriber import PeriodicDataSubscriber
from claraweb.monitoring.DpeMonitorCallBacks import RegDataCallBack, RunDataCallBack


logger = get_task_logger(__name__)
parser = ArgumentParser(description='Periodic Subscriber tasks')
parser.add_argument('data', type=str, help='registration or runtime data')
args = parser.parse_args()


def run_registration_subscriber():
    try:
        reg_subscriber = PeriodicDataSubscriber("RegDataSubscriber",
                                                "registration_topic")
        reg_subscription = reg_subscriber.subscribe(RegDataCallBack())
        xMsgUtil.log("WebServer Subscribed to registration messages...")
        xMsgUtil.keep_alive()

    except KeyboardInterrupt:
        reg_subscriber.unsubscribe(reg_subscription)
        reg_subscriber.destroy()
        xMsgUtil.log("WebServer: Registration subscription terminated")
        return


def run_runtime_subscriber():
    try:
        run_subscriber = PeriodicDataSubscriber("RunDataSubscriber",
                                                "runtime_topic")
        run_subscription = run_subscriber.subscribe(RunDataCallBack())
        xMsgUtil.log("WebServer Subscribed to runtime messages...")
        xMsgUtil.keep_alive()

    except KeyboardInterrupt:
        run_subscriber.unsubscribe(run_subscription)
        run_subscriber.destroy()
        xMsgUtil.log("WebServer: Runtime subscription terminated")
        return


def main():
    if args.data == "registration":
        run_registration_subscriber()
    elif args.data == "runtime":
        run_runtime_subscriber()
    else:
        print "usage: valid type options are \"registration\" or \"runtime\""
        return

if __name__ == "__main__":
    main()
