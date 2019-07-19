# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0045_articlefile'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='statistical_methods',
            field=models.TextField(max_length=1000, blank=True),
        ),
    ]
