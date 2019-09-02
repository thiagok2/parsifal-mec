# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0056_auto_20190830_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitorcomment',
            name='is_new',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='visitorcomment',
            name='parent',
            field=models.ForeignKey(related_name='parent_comment', to='reviews.VisitorComment', null=True),
        ),
    ]
