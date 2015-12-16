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

from xmsg.core.xMsgUtil import xMsgUtil

proj_path = os.path.abspath(os.path.dirname(__file__))[0:-19]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ClaraWebREST.settings")

sys.path.append(proj_path)
os.chdir(proj_path)
django.setup()


from claraweb.monitoring.base.PeriodicDataSubscriber import PeriodicDataSubscriber
from claraweb.monitoring.DpeMonitorCallBacks import DpeMonitorCallBack


def run_monitor_subscriber():
    try:
        topic = "dpeAlive:"
        topic = "registration_topic:%s" % xMsgUtil.get_local_ip()
        run_subscriber = PeriodicDataSubscriber(topic, topic)
        run_subscription = run_subscriber.subscribe(DpeMonitorCallBack())
        xMsgUtil.log("Subscribed to runtime messages with topic %s" % topic)
        xMsgUtil.keep_alive()

    except KeyboardInterrupt:
        run_subscriber.unsubscribe(run_subscription)
        run_subscriber.destroy()
        xMsgUtil.log("Runtime subscription terminated")
        return


def main():
    run_monitor_subscriber()


if __name__ == "__main__":
    main()
