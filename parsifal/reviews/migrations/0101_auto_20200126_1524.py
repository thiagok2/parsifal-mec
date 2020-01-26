# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0100_auto_20200126_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='statistical_methods',
            field=models.TextField(default=b'', max_length=1000, blank=True),
        ),
    ]
