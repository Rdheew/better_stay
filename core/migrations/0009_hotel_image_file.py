# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20151117_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='image_file',
            field=models.ImageField(null=True, upload_to=core.models.upload_to_location, blank=True),
        ),
    ]
