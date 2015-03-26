# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Service', '0003_auto_20150325_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='container_id',
            field=models.ForeignKey(related_name='services', to='Container.Container'),
            preserve_default=True,
        ),
    ]
