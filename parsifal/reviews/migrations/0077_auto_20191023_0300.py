# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0076_auto_20191023_0111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='a1',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=6, blank=True),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='a2',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=6, blank=True),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='dp1',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=6, blank=True),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='dp2',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=6, blank=True),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='effect_size',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=6, blank=True),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='max_limit',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=6, blank=True),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='min_limit',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=6, blank=True),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='std_error',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=6, blank=True),
        ),
    ]
