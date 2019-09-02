# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0057_auto_20190830_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitorcomment',
            name='is_open',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='visitorcomment',
            name='parent',
            field=models.ForeignKey(related_name='parent_comment', default=None, to='reviews.VisitorComment', null=True),
        ),
    ]
