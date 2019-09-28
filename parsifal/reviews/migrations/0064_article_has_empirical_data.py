# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0063_auto_20190926_0034'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='has_empirical_data',
            field=models.BooleanField(default=False),
        ),
    ]
