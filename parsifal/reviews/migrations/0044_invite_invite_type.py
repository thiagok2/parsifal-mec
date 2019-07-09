# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0043_invite'),
    ]

    operations = [
        migrations.AddField(
            model_name='invite',
            name='invite_type',
            field=models.CharField(default='visitor', max_length=100),
            preserve_default=False,
        ),
    ]
