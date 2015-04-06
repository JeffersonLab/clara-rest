# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Container', '0003_auto_20150325_1346'),
        ('Service', '0007_auto_20150405_2051'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceEngine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dpe_id', models.IntegerField(null=True)),
                ('engine_class', models.CharField(max_length=50, null=True)),
                ('configuration', models.TextField(default=b'')),
                ('threads', models.IntegerField(null=True)),
                ('created', models.DateTimeField(null=True)),
                ('modified', models.DateTimeField(null=True)),
                ('container_id', models.ForeignKey(related_name='services', to='Container.Container')),
            ],
            options={
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='serviceengineinfo',
            name='container_id',
        ),
        migrations.DeleteModel(
            name='ServiceEngineInfo',
        ),
    ]
