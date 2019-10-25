# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0077_auto_20191023_0300'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='articleevaluation',
            unique_together=set([('review', 'article', 'user')]),
        ),
    ]
