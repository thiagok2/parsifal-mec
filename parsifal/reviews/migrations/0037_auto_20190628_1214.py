# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0036_reviewtag'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reviewtag',
            options={'ordering': ('tag',), 'verbose_name': 'ReviewTag', 'verbose_name_plural': 'ReviewTags'},
        ),
        migrations.RenameField(
            model_name='reviewtag',
            old_name='description',
            new_name='tag',
        ),
    ]
