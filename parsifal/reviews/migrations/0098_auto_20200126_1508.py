# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0097_auto_20200126_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='objective',
            field=models.TextField(max_length=1000, blank=True),
        ),
    ]
