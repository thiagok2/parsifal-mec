# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0091_searchsession_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='related_to',
            field=models.CharField(blank=True, max_length=2, choices=[('P', 'Popula\xe7\xe3o'), ('I', 'Interven\xe7\xe3o'), ('C', 'Compara\xe7\xe3o'), ('O', 'Resultados'), ('S', 'Tipo de Estudo'), ('CT', 'Contexto')]),
        ),
    ]
