# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0019_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='entry_type',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name=b'Document type', choices=[(b'article', 'Article'), (b'book', 'Book'), (b'booklet', 'Booklet'), (b'conference', 'Conference'), (b'inbook', 'Inbook'), (b'incollection', 'Incollection'), (b'inproceedings', 'Inproceedings'), (b'manual', 'Manual'), (b'mastersthesis', "Master's Thesis"), (b'misc', 'Misc'), (b'phdthesis', 'Ph.D. Thesis'), (b'proceedings', 'Proceedings'), (b'techreport', 'Tech Report'), (b'unpublished', 'N\xe3o publicado')]),
        ),
    ]
