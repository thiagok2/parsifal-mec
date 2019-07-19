# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0045_articlefile'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleEvaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default='U', max_length=1, choices=[('U', 'Unclassified'), ('R', 'Rejected'), ('A', 'Accepted'), ('D', 'Duplicated')])),
                ('comments', models.TextField(max_length=2000, null=True, blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='article',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='article',
            name='selection_criteria',
        ),
        migrations.RemoveField(
            model_name='article',
            name='status',
        ),
        migrations.AddField(
            model_name='articleevaluation',
            name='article',
            field=models.ForeignKey(related_name='evaluation_article', to='reviews.Article'),
        ),
        migrations.AddField(
            model_name='articleevaluation',
            name='review',
            field=models.ForeignKey(related_name='evaluation_review', to='reviews.Review'),
        ),
        migrations.AddField(
            model_name='articleevaluation',
            name='selection_criteria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='reviews.SelectionCriteria', null=True),
        ),
        migrations.AddField(
            model_name='articleevaluation',
            name='user',
            field=models.ForeignKey(related_name='evaluation_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
