# coding=utf-8

from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from backend.rest.Container.models import Container
from backend.rest.Service.models import ServiceEngine
from backend.utils.minimal_orchestrator import MinimalOrchestrator


@receiver(pre_delete, sender=Container)
def remove_container_message_to_dpe(sender, instance=None,
                                    created=False, **kwargs):
    raw = kwargs.get('raw', False)
    if not raw:
        MinimalOrchestrator(instance.dpe.get_host(),
                            instance.dpe.get_proxy_port()).remove_container(instance)


@receiver(pre_save, sender=Container)
def deploy_container_message_to_dpe(sender, instance=None,
                                    created=False, **kwargs):
    raw = kwargs.get('raw', False)
    if not raw:
        try:
            MinimalOrchestrator(instance.dpe.get_host(),
                                instance.dpe.get_proxy_port()
                                ).deploy_container(instance)
        except:
            print "connection : %s at port %d " % (instance.dpe.get_host(),
                                                   instance.dpe.get_proxy_port())
            return


@receiver(pre_delete, sender=ServiceEngine)
def remove_service_message_to_dpe(sender, instance=None,
                                  created=False, **kwargs):
    try:
        raw = kwargs.get('raw', False)
        if not raw:
            MinimalOrchestrator(instance.container.dpe.get_host(),
                               instance.container.dpe.get_proxy_port()).remove_service(instance)
    except:
        print "connection : %s at port %d " % (instance.container.dpe.get_host(),
                                               instance.container.dpe.get_proxy_port())
        return


@receiver(pre_save, sender=ServiceEngine)
def deploy_service_message_to_dpe(sender, instance=None,
                                  created=False, **kwargs):
    raw = kwargs.get('raw', False)
    try:
        if not raw:
            MinimalOrchestrator(instance.container.dpe.get_host(),
                                instance.container.dpe.get_proxy_port()).deploy_service(instance)
    except:
        print "connection : %s at port %d " % (instance.container.dpe.get_host(),
                                               instance.container.dpe.get_proxy_port())
        return
