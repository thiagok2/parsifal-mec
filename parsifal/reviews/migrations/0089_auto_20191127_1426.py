# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0088_auto_20191118_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='deleted',
            field=models.DateTimeField(null=True, editable=False),
        ),
        migrations.AddField(
            model_name='source',
            name='deleted',
            field=models.DateTimeField(null=True, editable=False),
        ),
    ]
