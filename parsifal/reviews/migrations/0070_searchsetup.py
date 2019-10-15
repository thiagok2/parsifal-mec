# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0069_auto_20191012_0309'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchSetup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('conclusion_model', models.CharField(default='HATTIE', max_length=10, choices=[('COHEN', 'Cohen'), ('HATTIE', 'Hattie')])),
                ('adverse_effect', models.CharField(max_length=150)),
                ('no_effect', models.CharField(max_length=150)),
                ('small_effect', models.CharField(max_length=150)),
                ('intermediate_effect', models.CharField(max_length=150)),
                ('large_effect', models.CharField(max_length=150)),
                ('developmental_effects', models.CharField(max_length=150)),
                ('teacher_effects', models.CharField(max_length=150)),
                ('zone_desired_effects', models.CharField(max_length=150)),
                ('review', models.OneToOneField(to='reviews.Review')),
            ],
            options={
                'verbose_name': 'Search Setup',
                'verbose_name_plural': 'Search Setups',
            },
        ),
    ]
