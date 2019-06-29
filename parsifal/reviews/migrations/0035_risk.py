# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0034_auto_20170809_2034'),
    ]

    operations = [
        migrations.CreateModel(
            name='Risk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('risk', models.CharField(max_length=500)),
                ('order', models.IntegerField(default=0)),
                ('parent_risk', models.ForeignKey(related_name='+', to='reviews.Risk', null=True)),
                ('review', models.ForeignKey(related_name='risks_to_review_validity', to='reviews.Review')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Risk',
                'verbose_name_plural': 'Risks',
            },
        ),
    ]
