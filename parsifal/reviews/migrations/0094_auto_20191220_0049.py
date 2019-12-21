# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0093_auto_20191220_0029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='distributed_to',
        ),
        migrations.AddField(
            model_name='article',
            name='distributed_to',
            field=models.ForeignKey(related_name='distributed_to', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
