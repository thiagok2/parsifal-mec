# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0072_auto_20191017_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleempiricaldata',
            name='data_type',
            field=models.CharField(default='U', max_length=100, choices=[('U', 'Primary data'), ('R', 'Precalculated Effect Size')]),
        ),
        migrations.AddField(
            model_name='articleempiricaldata',
            name='effect_size',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='articleempiricaldata',
            name='max_limit',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='articleempiricaldata',
            name='min_limit',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True),
        ),
    ]
