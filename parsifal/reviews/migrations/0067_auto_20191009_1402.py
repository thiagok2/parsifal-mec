# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0066_auto_20191008_0143'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleempiricaldata',
            name='a1',
            field=models.DecimalField(default=1, max_digits=3, decimal_places=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='articleempiricaldata',
            name='a2',
            field=models.DecimalField(default=1, max_digits=3, decimal_places=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='articleempiricaldata',
            name='dp1',
            field=models.DecimalField(default=1, max_digits=3, decimal_places=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='articleempiricaldata',
            name='dp2',
            field=models.DecimalField(default=1, max_digits=3, decimal_places=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='articleempiricaldata',
            name='n1',
            field=models.DecimalField(default=1, max_digits=3, decimal_places=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='articleempiricaldata',
            name='n2',
            field=models.DecimalField(default=1, max_digits=3, decimal_places=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='keyword',
            name='related_to',
            field=models.CharField(blank=True, max_length=1, choices=[('P', 'Popula\xe7\xe3o'), ('I', 'Interven\xe7\xe3o'), ('C', 'Compara\xe7\xe3o'), ('O', 'Resultados'), ('S', 'Tipo de Estudo'), ('CT', 'Contexto')]),
        ),
    ]
