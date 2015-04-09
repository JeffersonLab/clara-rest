# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('app_id', models.AutoField(serialize=False, primary_key=True)),
                ('chain', models.TextField(default=b'')),
                ('registered_class', models.CharField(default=b'', max_length=50)),
                ('created', models.DateTimeField(null=True)),
                ('modified', models.DateTimeField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
