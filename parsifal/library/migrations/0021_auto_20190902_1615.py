# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0020_auto_20190830_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='entry_type',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name=b'Document type', choices=[(b'article', 'Article (Artigo de um peri\xf3dico ou revista)'), (b'book', 'Book (Livro)'), (b'booklet', 'Booklet (Livreto n\xe3o distribu\xeddo)'), (b'conference', 'Conference (Confer\xeancia)'), (b'inbook', 'Inbook (Cap\xedtulo ou Se\xe7\xe3o)'), (b'incollection', 'Incollection (Uma parte de um livro que possui t\xedtulo pr\xf3prio)'), (b'inproceedings', 'Inproceedings (Um artigo nos anais de uma confer\xeancia)'), (b'manual', 'Manual (Documenta\xe7\xe3o T\xe9cnica)'), (b'mastersthesis', "Master's Thesis (Disserta\xe7\xe3o de Mestrado)"), (b'misc', 'Misc (Miscel\xe2nea)'), (b'phdthesis', 'Ph.D. Thesis (Tese de Doutorado)'), (b'proceedings', 'Proceedings (Anais de uma confer\xeancia)'), (b'techreport', 'Tech Report (Relat\xf3rio T\xe9cnico)'), (b'unpublished', 'Unpublished (N\xe3o publicado)')]),
        ),
    ]
