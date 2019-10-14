# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0068_auto_20191012_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='n1',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='n2',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
