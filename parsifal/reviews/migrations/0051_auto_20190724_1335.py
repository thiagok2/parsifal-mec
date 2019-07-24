# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0050_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='study',
            name='status',
            field=models.CharField(default='U', max_length=1, choices=[('U', 'N\xe3o classificado'), ('R', 'Rejeitado'), ('A', 'Accepted'), ('D', 'Duplicated')]),
        ),
    ]
