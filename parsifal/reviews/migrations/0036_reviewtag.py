# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0035_risk'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=300)),
                ('review', models.ForeignKey(related_name='review_tags', to='reviews.Review')),
            ],
            options={
                'ordering': ('description',),
                'verbose_name': 'ReviewTag',
                'verbose_name_plural': 'ReviewTags',
            },
        ),
    ]
