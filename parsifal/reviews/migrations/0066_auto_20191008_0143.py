# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0065_auto_20191004_0244'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleEmpiricalData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('article', models.ForeignKey(related_name='empirical_article', to='reviews.Article')),
            ],
            options={
                'ordering': ('article',),
                'verbose_name': 'Article Empirical Data',
                'verbose_name_plural': 'Articles Empirical Data',
            },
        ),
        migrations.AddField(
            model_name='review',
            name='is_metaanalysis',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='articleempiricaldata',
            name='review',
            field=models.ForeignKey(related_name='empirical_review', to='reviews.Review'),
        ),
    ]
