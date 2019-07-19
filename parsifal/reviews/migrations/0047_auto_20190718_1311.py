# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0046_auto_20190717_2301'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articleevaluation',
            options={'ordering': ('status',), 'verbose_name': 'ArticleEvaluation', 'verbose_name_plural': 'ArticleEvaluations'},
        ),
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.CharField(default='U', max_length=1, choices=[('U', 'Unclassified'), ('W', 'Waiting'), ('R', 'Rejected'), ('A', 'Accepted'), ('D', 'Duplicated'), ('C', 'Conflict')]),
        ),
    ]
