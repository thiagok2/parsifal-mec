# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0040_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='visitors',
            field=models.ManyToManyField(related_name='visitors', to=settings.AUTH_USER_MODEL),
        ),
    ]
