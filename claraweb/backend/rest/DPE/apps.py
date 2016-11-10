# coding=utf-8

from django.apps import AppConfig


class DPEConfig(AppConfig):
    name = 'claraweb.backend.rest.DPE'
    verbose_name = 'DPE'

    def ready(self):
        import signals
