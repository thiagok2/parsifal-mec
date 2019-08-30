# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0051_auto_20190724_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='pico_text',
            field=models.CharField(max_length=1000, blank=True),
        ),
        migrations.AddField(
            model_name='review',
            name='pico_type',
            field=models.CharField(default='PICOC', max_length=200, choices=[('PICOC', 'PICOC'), ('PICOS', 'PICOS'), ('Free Text', 'Free Text')]),
        ),
        migrations.AddField(
            model_name='review',
            name='study_type',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(default='U', max_length=1, choices=[('U', 'N\xe3o classificado'), ('W', 'Aguardando'), ('R', 'Rejeitado'), ('A', 'Aceito'), ('D', 'Duplicado'), ('C', 'Conflito')]),
        ),
        migrations.AlterField(
            model_name='articleevaluation',
            name='status',
            field=models.CharField(default='U', max_length=1, choices=[('U', 'N\xe3o classificado'), ('R', 'Rejeitado'), ('A', 'Aceito'), ('D', 'Duplicado')]),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='related_to',
            field=models.CharField(blank=True, max_length=1, choices=[('P', 'Popula\xe7\xe3o'), ('I', 'Interven\xe7\xe3o'), ('C', 'Compara\xe7\xe3o'), ('O', 'Resultados')]),
        ),
        migrations.AlterField(
            model_name='review',
            name='status',
            field=models.CharField(default='U', max_length=1, choices=[('U', 'Unpublished (N\xe3o publicado)'), ('P', 'Publicado')]),
        ),
        migrations.AlterField(
            model_name='selectioncriteria',
            name='criteria_type',
            field=models.CharField(max_length=1, choices=[('I', 'Inclus\xe3o'), ('E', 'Exclus\xe3o')]),
        ),
        migrations.AlterField(
            model_name='study',
            name='status',
            field=models.CharField(default='U', max_length=1, choices=[('U', 'N\xe3o classificado'), ('R', 'Rejeitado'), ('A', 'Aceito'), ('D', 'Duplicado')]),
        ),
    ]
