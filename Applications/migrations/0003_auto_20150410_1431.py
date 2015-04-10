# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Applications', '0002_auto_20150409_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='input',
            field=models.FilePathField(default=b'', path=b'/work/input/', match=b'*.bin'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='app',
            name='output',
            field=models.FilePathField(default=b'', path=b'/work/output/', match=b'*.bin'),
            preserve_default=True,
        ),
    ]
