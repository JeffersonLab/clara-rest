# coding=utf-8

from django.db import models

from claraweb.rest.DPE.models import DPE
from claraweb.web_backend.orchestrators.orchestrator import RESTOrchestrator
from claraweb.web_backend.utils.Validators import validate_node_existence


class Container(models.Model):
    container_id = models.AutoField(primary_key=True, null=False)
    dpe = models.ForeignKey(DPE, related_name='containers',
                            validators=[validate_node_existence])
    author = models.CharField(blank=False, max_length=40)
    name = models.CharField(blank=False, max_length=40)

    start_time = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)

    class Meta:
        unique_together = ('dpe', 'name')

    def __str__(self):
        return self.get_canonical_name()

    def get_dpe_name(self):
        return str(self.dpe)

    def get_language(self):
        return str(self.dpe.language)

    def get_canonical_name(self):
        return str(self.get_dpe_name() + ":" + self.name)

    def save(self, *args, **kwargs):
        orchestrator = RESTOrchestrator()
        orchestrator.deploy_container(self.get_dpe_name(), self.name)
        super(Container, self).save(*args, **kwargs)