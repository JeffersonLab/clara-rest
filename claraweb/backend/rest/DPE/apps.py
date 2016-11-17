# coding=utf-8

from django.apps import AppConfig


class DPEConfig(AppConfig):
    name = 'backend.rest.DPE'
    verbose_name = 'DPE'

    def ready(self):
        import signals
