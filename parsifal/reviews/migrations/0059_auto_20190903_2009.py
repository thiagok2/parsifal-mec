# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0058_auto_20190831_0208'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentSeen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'ordering': ('user',),
                'verbose_name': 'Comment Seen',
                'verbose_name_plural': 'Comments Seen',
            },
        ),
        migrations.RemoveField(
            model_name='visitorcomment',
            name='is_new',
        ),
        migrations.AlterField(
            model_name='visitorcomment',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AddField(
            model_name='commentseen',
            name='comment',
            field=models.ForeignKey(related_name='comment_usercomments', to='reviews.VisitorComment'),
        ),
        migrations.AddField(
            model_name='commentseen',
            name='review',
            field=models.ForeignKey(related_name='review_usercomments', to='reviews.Review'),
        ),
        migrations.AddField(
            model_name='commentseen',
            name='user',
            field=models.ForeignKey(related_name='user_usercomments', to=settings.AUTH_USER_MODEL),
        ),
    ]
