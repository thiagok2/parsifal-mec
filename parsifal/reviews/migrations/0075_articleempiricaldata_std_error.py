# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0074_auto_20191023_0045'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleempiricaldata',
            name='std_error',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=3, blank=True),
        ),
    ]
