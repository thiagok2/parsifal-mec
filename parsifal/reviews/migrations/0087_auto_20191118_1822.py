# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0086_auto_20191113_0221'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 18, 18, 22, 13, 354883, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='source',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 18, 18, 22, 25, 4825, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='articleevaluation',
            name='article',
            field=models.ForeignKey(to='reviews.Article'),
        ),
    ]
