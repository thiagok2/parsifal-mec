# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0104_auto_20200128_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='comparison',
            field=models.CharField(default=None, max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='context',
            field=models.CharField(default=None, max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='intervention',
            field=models.CharField(default=None, max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='outcome',
            field=models.CharField(default=None, max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='population',
            field=models.CharField(default=None, max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='study_type',
            field=models.CharField(default=None, max_length=200, blank=True),
        ),
    ]
