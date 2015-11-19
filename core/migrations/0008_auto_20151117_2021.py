# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_review_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hotel',
            old_name='title',
            new_name='hotel',
        ),
    ]
