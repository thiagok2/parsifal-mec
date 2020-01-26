# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0101_auto_20200126_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='statistical_methods',
            field=models.TextField(max_length=1000, null=True, blank=True),
        ),
    ]
