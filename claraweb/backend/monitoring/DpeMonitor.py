#!/usr/bin/env python
# coding=utf-8

import os
import sys
import django
from xmsg.core.xMsgUtil import xMsgUtil

proj_path = os.path.abspath(os.path.dirname(__file__))[0:-27]
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "claraweb.backend.settings")

sys.path.append(proj_path)
os.chdir(proj_path)
django.setup()


from claraweb.backend.monitoring.base.PeriodicDataSubscriber import PeriodicDataSubscriber
from claraweb.backend.monitoring.DpeMonitorCallBacks import DpeMonitorCallBack


def run_monitor_subscriber():
    """Starts the clara subscription for monitoring"""
    run_subscriber = None
    run_subscription = None

    try:
        topic = "dpeReport"
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
