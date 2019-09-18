# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0061_auto_20190906_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='related_to',
            field=models.CharField(blank=True, max_length=1, choices=[('P', 'Popula\xe7\xe3o'), ('I', 'Interven\xe7\xe3o'), ('C', 'Compara\xe7\xe3o'), ('O', 'Resultados'), ('S', 'Tipo de Estudo')]),
        ),
        migrations.AlterField(
            model_name='review',
            name='pico_type',
            field=models.CharField(default=b'PICOC', max_length=200, choices=[(b'PICOC', 'PICOC'), (b'PICOS', 'PICOS'), (b'Free Text', 'Texto Livre')]),
        ),
        migrations.AlterField(
            model_name='visitorcomment',
            name='about',
            field=models.CharField(max_length=50, choices=[('OBJECTIVES', 'Objetivos'), ('PICOC', 'PICOC'), ('QUESTIONS', 'Quest\xf5es de Pesquisa'), ('KEYWORDS', 'Palavras-chaves e Sin\xf4nimos'), ('SEARCH_STRING', 'String de Busca'), ('SOURCES', 'Fontes'), ('CRITERIA', 'Crit\xe9rios de Sele\xe7\xe3o'), ('QA_QUESTIONS', 'Quest\xf5es de Checklist de Avalia\xe7\xe3o de Qualidade'), ('QA_ANSWERS', 'Respostas do Checklist de Avalia\xe7\xe3o de Qualidade'), ('QA_SCORES', 'Pontua\xe7\u1ebdos do Checklist de Avalia\xe7\xe3o de Qualidade'), ('RISKS', 'Riscos a Validade da Revis\xe3o'), ('DATA_EXTRACTION_FORM', 'Formul\xe1rio de Extra\xe7\xe3o de Dados'), ('STATISTICAL_METHODS', 'M\xe9todos Estat\xedsticos e Conven\xe7\xf5es'), ('CONDUCTING_SEARCH', 'Condu\xe7\xe3o da Pesquisa'), ('IMPORT_STUDIES', 'Importar Estudos'), ('STUDY_SELECTION', 'Sele\xe7\xe3o de Estudos'), ('QUALITY_ASSESSMENT', 'Avalia\xe7\xe3o de Qualidade'), ('DATA_EXTRACTION', 'Extra\xe7\xe3o de Dados'), ('DATA_ANALYSIS', 'An\xe1lise de Dados')]),
        ),
    ]
