# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_auto_20200126_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='institution',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='url',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
