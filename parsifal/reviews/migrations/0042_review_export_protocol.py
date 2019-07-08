# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0041_review_visitors'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='export_protocol',
            field=models.BooleanField(default=False),
        ),
    ]
