# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Container', '0003_auto_20150325_1346'),
        ('Service', '0004_auto_20150326_1318'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('options', models.TextField(default=b'[]')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ServiceEngineInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dpe_id', models.IntegerField(null=True)),
                ('service_class', models.CharField(max_length=50, null=True)),
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
            model_name='service',
            name='container_id',
        ),
        migrations.DeleteModel(
            name='Service',
        ),
    ]
