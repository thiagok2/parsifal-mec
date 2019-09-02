# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0058_auto_20190831_0208'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='export_pico',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='review',
            name='status',
            field=models.CharField(default='U', max_length=1, choices=[('U', 'Unpublished (N\xe3o publicado)'), ('P', 'Publicado')]),
        ),
        migrations.AlterField(
            model_name='visitorcomment',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
