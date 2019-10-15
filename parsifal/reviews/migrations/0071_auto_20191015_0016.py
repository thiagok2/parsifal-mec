# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0070_searchsetup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchsetup',
            name='review',
            field=models.ForeignKey(to='reviews.Review'),
        ),
    ]
