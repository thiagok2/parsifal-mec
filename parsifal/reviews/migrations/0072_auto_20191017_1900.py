# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0071_auto_20191015_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='a1',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='a2',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='dp1',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='dp2',
            field=models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True),
        ),
    ]
