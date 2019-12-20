# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0092_auto_20191209_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='distributed_to',
            field=models.ForeignKey(related_name='distributed_to', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='data_type',
            field=models.CharField(default='P', max_length=100, choices=[('P', 'Primary data'), ('E', 'Precalculated Effect Size')]),
        ),
    ]
