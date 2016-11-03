# coding=utf-8

from django.core.exceptions import ValidationError
from claraweb.backend.rest.DPE.models import DPE
from claraweb.backend.utils.CWConstants import DPE_CREATION_LIMIT


def limit_validator(value):
    if value > DPE_CREATION_LIMIT:
        raise ValidationError(u'%s bigger than the DPE creation limit' % value)


def validate_node_existence(node_id):
    try:
        DPE.objects.get(node_id=node_id)
    except DPE.DoesNotExist:
        raise ValidationError(u'Dpe node must be registered and available')
