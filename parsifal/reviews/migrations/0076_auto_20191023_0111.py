# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0075_articleempiricaldata_std_error'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='effect_size',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='max_limit',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='min_limit',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='std_error',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True),
        ),
    ]
