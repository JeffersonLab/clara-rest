# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Container', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='name',
            field=models.CharField(max_length=20, null=True),
            preserve_default=True,
        ),
    ]
