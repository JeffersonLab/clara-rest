# coding=utf-8

from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from claraweb.backend.rest.Container.models import Container
from claraweb.backend.rest.Service.models import ServiceEngine
from claraweb.backend.utils.minimal_orchestrator import MinimalOrchestrator


@receiver(pre_delete, sender=Container)
def remove_container_message_to_dpe(sender, instance=None,
                                    created=False, **kwargs):
    MinimalOrchestrator(instance.dpe.get_host(),
                        instance.dpe.get_proxy_port()).remove_container(instance)


@receiver(pre_save, sender=Container)
def deploy_container_message_to_dpe(sender, instance=None,
                                    created=False, **kwargs):
    MinimalOrchestrator(instance.dpe.get_host(),
                        instance.dpe.get_proxy_port()
                        ).deploy_container(instance)


@receiver(pre_delete, sender=ServiceEngine)
def remove_service_message_to_dpe(sender, **kwargs):
    MinimalOrchestrator(sender.dpe.get_host(),
                        sender.dpe.get_proxy_port()).remove_service(sender)


@receiver(pre_save, sender=ServiceEngine)
def deploy_service_message_to_dpe(sender, **kwargs):
    MinimalOrchestrator(sender.dpe.get_host(),
                        sender.dpe.get_proxy_port()).deploy_service(sender)
