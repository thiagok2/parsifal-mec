# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0037_auto_20190628_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=300)),
                ('review', models.ForeignKey(related_name='review_tags', to='reviews.Review')),
            ],
            options={
                'ordering': ('tag',),
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.RemoveField(
            model_name='reviewtag',
            name='review',
        ),
        migrations.DeleteModel(
            name='ReviewTag',
        ),
    ]
