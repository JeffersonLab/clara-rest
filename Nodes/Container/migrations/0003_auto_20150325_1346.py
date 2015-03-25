# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Container', '0002_container_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='dpe_id',
            field=models.ForeignKey(related_name='containers', to='Nodes.Node'),
            preserve_default=True,
        ),
    ]
