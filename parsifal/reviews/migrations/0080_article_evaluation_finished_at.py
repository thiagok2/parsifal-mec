# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0079_auto_20191026_0044'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='evaluation_finished_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
