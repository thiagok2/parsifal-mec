# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0067_auto_20191009_1402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articleempiricaldata',
            name='id',
        ),
        migrations.RemoveField(
            model_name='articleempiricaldata',
            name='review',
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='a1',
            field=models.DecimalField(null=True, max_digits=3, decimal_places=1, blank=True),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='a2',
            field=models.DecimalField(null=True, max_digits=3, decimal_places=1, blank=True),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='article',
            field=models.OneToOneField(primary_key=True, serialize=False, to='reviews.Article'),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='dp1',
            field=models.DecimalField(null=True, max_digits=3, decimal_places=1, blank=True),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='dp2',
            field=models.DecimalField(null=True, max_digits=3, decimal_places=1, blank=True),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='n1',
            field=models.DecimalField(null=True, max_digits=3, decimal_places=1, blank=True),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='n2',
            field=models.DecimalField(null=True, max_digits=3, decimal_places=1, blank=True),
        ),
    ]
