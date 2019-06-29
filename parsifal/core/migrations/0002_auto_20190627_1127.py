# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='media_type',
            field=models.CharField(max_length=5, choices=[('image', 'Imagem'), ('video', 'Video')]),
        ),
    ]
