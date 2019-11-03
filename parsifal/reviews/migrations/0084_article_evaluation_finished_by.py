# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0083_auto_20191029_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='evaluation_finished_by',
            field=models.ForeignKey(related_name='articles_resolved', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
