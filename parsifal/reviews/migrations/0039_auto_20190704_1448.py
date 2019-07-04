# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0038_auto_20190628_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='export_dataextraction',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='review',
            name='export_qualityassessment',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='review',
            name='export_risks',
            field=models.BooleanField(default=False),
        ),
    ]
