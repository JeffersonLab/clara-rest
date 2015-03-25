# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Service', '0002_service_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='name',
        ),
        migrations.AddField(
            model_name='service',
            name='service_class',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
    ]
