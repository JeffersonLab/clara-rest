# coding=utf-8

from django.core.management.base import BaseCommand
from claraweb.backend.monitoring.DpeMonitor import run_monitor_subscriber


class Command(BaseCommand):
    """Command to start the Clara DPE monitoring subscription"""
    help = "Starts DPE Monitoring Subscription"

    def handle(self, *args, **options):
        run_monitor_subscriber()
