# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0060_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='qualityanswer',
            name='question',
            field=models.ForeignKey(default=1, to='reviews.QualityQuestion'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='commentseen',
            name='comment',
            field=models.ForeignKey(related_name='comment_seencomments', to='reviews.VisitorComment'),
        ),
        migrations.AlterField(
            model_name='commentseen',
            name='review',
            field=models.ForeignKey(related_name='review_seencomments', to='reviews.Review'),
        ),
        migrations.AlterField(
            model_name='commentseen',
            name='user',
            field=models.ForeignKey(related_name='user_seencomments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='related_to',
            field=models.CharField(blank=True, max_length=1, choices=[('P', 'Popula\xe7\xe3o'), ('I', 'Interven\xe7\xe3o'), ('C', 'Compara\xe7\xe3o'), ('O', 'Resultados'), ('S', 'Study Type')]),
        ),
    ]
