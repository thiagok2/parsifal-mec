# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_profile_public_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='institution',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='url',
            field=models.CharField(default=b'', max_length=50),
        ),
    ]
