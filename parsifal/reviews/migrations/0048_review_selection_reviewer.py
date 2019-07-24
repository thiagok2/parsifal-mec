# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0047_auto_20190718_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='selection_reviewer',
            field=models.ForeignKey(related_name='selection_reviewer', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
