# coding=utf-8
from optparse import make_option

from django.core.management.base import BaseCommand
from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.net.xMsgAddress import ProxyAddress

from claraweb.backend.monitoring.DpeMonitorCallBacks import DpeMonitorCallBack


class Command(BaseCommand):
    """Command to start the Clara DPE monitoring subscription"""
    help = "Starts DPE Monitoring Subscription"

    option_list = BaseCommand.option_list + (
        make_option(
            "-f",
            "--fe_host",
            dest="fe_host",
            help="specify frontend host",
            metavar="STRING"
        ),
    )

    def handle(self, *args, **options):
        if not options['fe_host']:
            fe_host = "localhost"

        else:
            xMsgUtil.log("Now monitoring frontend:%s" % options['fe_host'])
            fe_host = options['fe_host']

        topic = xMsgTopic.build("dpeReport")
        subscriber = xMsg("ReportSubscriber")
        subscription = None

        try:
            subscription = subscriber.subscribe(ProxyAddress(fe_host),
                                                topic, DpeMonitorCallBack())
            xMsgUtil.log("Subscribed to runtime messages with topic dpeReport")
            xMsgUtil.keep_alive()

        except KeyboardInterrupt:
            subscriber.unsubscribe(subscription)
            subscriber.destroy()
            xMsgUtil.log("Runtime subscription terminated")
