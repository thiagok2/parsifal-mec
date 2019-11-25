# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0087_auto_20191118_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='source',
            name='last_update',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
