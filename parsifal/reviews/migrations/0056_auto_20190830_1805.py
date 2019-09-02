# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0055_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitorcomment',
            name='to',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='status',
            field=models.CharField(default='U', max_length=1, choices=[('U', 'N\xe3o publicado'), ('P', 'Publicado')]),
        ),
    ]
