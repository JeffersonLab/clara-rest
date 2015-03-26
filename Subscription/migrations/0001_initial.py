# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionHandler',
            fields=[
                ('subscription_id', models.AutoField(serialize=False, primary_key=True)),
                ('type', models.CharField(default=b'INFO', max_length=10, choices=[(b'INFO', b'INFO'), (b'WARNING', b'WARNING'), (b'ERROR', b'ERROR'), (b'DATA', b'DATA'), (b'DONE', b'DONE')])),
                ('sender', models.CharField(default=b'CLOUD', max_length=30)),
                ('created', models.DateTimeField(null=True)),
                ('modified', models.DateTimeField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
