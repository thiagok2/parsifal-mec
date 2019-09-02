# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0053_visitorcomment_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='visitorcomment',
            options={'ordering': ('-date',), 'verbose_name': 'Visitor Comment', 'verbose_name_plural': 'Visitor Comments'},
        ),
    ]
