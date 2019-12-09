# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0090_articleevaluation_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchsession',
            name='deleted',
            field=models.DateTimeField(null=True, editable=False),
        ),
    ]
