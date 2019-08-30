# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0052_auto_20190830_0047'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitorcomment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 30, 1, 41, 53, 892737, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
