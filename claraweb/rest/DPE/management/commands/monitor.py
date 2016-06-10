# coding=utf-8
from optparse import make_option

from django.core.management.base import BaseCommand
from claraweb.backend.monitoring.DpeMonitor import run_monitor_subscriber


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
            run_monitor_subscriber()
        else:
            print "Now monitoring frontend:%s" % options['fe_host']
            run_monitor_subscriber(options['fe_host'])
