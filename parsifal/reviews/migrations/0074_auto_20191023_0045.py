# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0073_auto_20191022_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='data_type',
            field=models.CharField(default='P', max_length=100, choices=[('P', 'Primary data'), ('E', 'Precalculated Effect Size')]),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='effect_size',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=3, blank=True),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='max_limit',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=3, blank=True),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='min_limit',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=3, blank=True),
        ),
    ]
