# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0078_auto_20191025_1058'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleevaluation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='articleevaluation',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
