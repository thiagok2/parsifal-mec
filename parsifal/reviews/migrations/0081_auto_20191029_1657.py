# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0080_article_evaluation_finished_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='data_type',
            field=models.CharField(default='P', max_length=100, choices=[('P', 'Dados prim\xe1rios'), ('E', 'Tamanho do Efeito pr\xe9-calculados')]),
        ),
    ]
