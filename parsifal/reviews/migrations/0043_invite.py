# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0042_review_export_protocol'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=500)),
                ('review', models.ForeignKey(related_name='review_invites', to='reviews.Review')),
            ],
            options={
                'ordering': ('email',),
                'verbose_name': 'Invite',
                'verbose_name_plural': 'Invites',
            },
        ),
    ]
