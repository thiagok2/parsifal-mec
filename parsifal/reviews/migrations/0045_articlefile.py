# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import parsifal.reviews.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0044_invite_invite_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('article_file', models.FileField(upload_to=parsifal.reviews.models.article_directory_path)),
                ('name', models.CharField(max_length=300)),
                ('size', models.CharField(max_length=150)),
                ('article', models.ForeignKey(related_name='file_article', to='reviews.Article')),
                ('review', models.ForeignKey(related_name='file_review', to='reviews.Review')),
                ('user', models.ForeignKey(related_name='file_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
