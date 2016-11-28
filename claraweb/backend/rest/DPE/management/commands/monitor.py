# coding=utf-8

import datetime

from django.core.management.base import BaseCommand
from influxdb import InfluxDBClient
from optparse import make_option
from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.net.xMsgAddress import ProxyAddress

from backend.monitoring.monitor_callBacks import DpeMonitorCallBack
from backend.rest.DPE.models import DPE


class Command(BaseCommand):
    """Command to start the Clara DPE monitoring subscription"""
    help = "Starts DPE Monitoring Subscription"

    option_list = BaseCommand.option_list + (
        make_option(
            "-f",
            "--fe-host",
            dest="fe_host",
            help="Specify frontend host to monitor",
            metavar="STRING"
        ),
        make_option(
            "-s",
            "--sync-influx-db",
            dest="sync_db",
            action="store_true",
            help="Sync the Influx database. It will recreate the runtimen db.",
        ),
        make_option(
            "-c",
            "--clean-old-data",
            dest="clean_old_data",
            action="store_true",
            help="Remove old data from the django database.",
        ),
        make_option(
            "-d",
            "--db-host",
            dest="db_host",
            action="store_true",
            help="Specify influxdb host",
            default="localhost",
            metavar = "STRING"
        ),
    )

    def handle(self, *args, **options):
        if options['clean_old_data']:
            # Data TTL = Ten minutes
            delta = datetime.datetime.now() - datetime.timedelta(minutes=10)

            count = 0
            for dpe in DPE.objects.filter(modified__lt=delta):
                for container in dpe.containers.all():
                    for service in container.services.all():
                        service.delete()
                        count += 1
                    container.delete()
                    count += 1
                dpe.delete()
                count += 1
            print "%d registers deleted..." % count
            return

        if options['sync_db']:
            db = "claraRuntime"
            client = InfluxDBClient(database=db)
            client.drop_database(db)
            client.create_database(db)

        if not options['fe_host']:
            fe_host = "localhost"

        else:
            xMsgUtil.log("Now monitoring frontend:%s" % options['fe_host'])
            fe_host = options['fe_host']

        topic = xMsgTopic.build("dpeReport")
        subscriber = xMsg("ReportSubscriber")
        subscription = None

        try:
            subscription = subscriber.subscribe(ProxyAddress(fe_host, 7771),
                                                topic, DpeMonitorCallBack('192.168.0.2'))
            xMsgUtil.log("Subscribed to runtime messages with topic dpeReport")

        except KeyboardInterrupt:
            subscriber.unsubscribe(subscription)
            subscriber.destroy()
            xMsgUtil.log("Runtime data subscription terminated")
