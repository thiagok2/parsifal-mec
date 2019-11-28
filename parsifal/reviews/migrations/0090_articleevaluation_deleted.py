# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0089_auto_20191127_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleevaluation',
            name='deleted',
            field=models.DateTimeField(null=True, editable=False),
        ),
    ]
