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


def run_monitor_subscriber(fe_host="localhost"):
    """Starts the clara subscription for monitoring"""
    run_subscriber = None
    run_subscription = None

    try:
        run_subscriber = PeriodicDataSubscriber(fe_host, "dpeReport")
        run_subscription = run_subscriber.subscribe_to_frontend(DpeMonitorCallBack())
        xMsgUtil.log("Subscribed to runtime messages with topic dpeReport.")

    except KeyboardInterrupt:
        run_subscriber.unsubscribe(run_subscription)
        run_subscriber.destroy()
        xMsgUtil.log("Runtime subscription terminated")
        return
