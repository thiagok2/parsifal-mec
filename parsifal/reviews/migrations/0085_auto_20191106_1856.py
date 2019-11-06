# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0084_article_evaluation_finished_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='data_type',
            field=models.CharField(default='P', max_length=100, choices=[('P', 'Primary data'), ('E', 'Precalculated Effect Size')]),
        ),
    ]
