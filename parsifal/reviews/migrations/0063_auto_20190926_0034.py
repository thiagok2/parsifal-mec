# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0062_auto_20190918_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataextractionfield',
            name='field_type',
            field=models.CharField(max_length=1, choices=[(b'B', 'Campo Boleano'), (b'S', 'Campo de Texto'), (b'F', 'Campo Num\xe9rico (Ponto Flutuante)'), (b'I', 'Campo Num\xe9rico (Inteiro)'), (b'D', 'Campo de Data'), (b'O', 'Campo Selecion\xe1vel'), (b'M', 'Campo Multipla Escolha')]),
        ),
    ]
