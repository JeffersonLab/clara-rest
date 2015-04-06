# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Service', '0005_auto_20150331_1833'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ServiceConfiguration',
            new_name='ServiceEngineConfiguration',
        ),
        migrations.AddField(
            model_name='serviceengineinfo',
            name='service_configuration',
            field=models.TextField(default=b'[]'),
            preserve_default=True,
        ),
    ]
