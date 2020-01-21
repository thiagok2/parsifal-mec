# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0094_auto_20191220_0049'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleReviewer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('article', models.ForeignKey(to='reviews.Article')),
                ('review', models.ForeignKey(to='reviews.Review')),
                ('reviewer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='articleempiricaldata',
            name='data_type',
            field=models.CharField(default='P', max_length=100, choices=[('P', 'Dados prim\xe1rios'), ('E', 'Tamanho do Efeito pr\xe9-calculados')]),
        ),
    ]
