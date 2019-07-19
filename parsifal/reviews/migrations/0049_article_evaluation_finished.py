# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0048_review_selection_reviewer'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='evaluation_finished',
            field=models.BooleanField(default=False),
        ),
    ]
