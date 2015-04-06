# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Service', '0006_auto_20150405_2036'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ServiceEngineConfiguration',
        ),
        migrations.RenameField(
            model_name='serviceengineinfo',
            old_name='service_configuration',
            new_name='configuration',
        ),
        migrations.RenameField(
            model_name='serviceengineinfo',
            old_name='service_class',
            new_name='engine_class',
        ),
    ]
