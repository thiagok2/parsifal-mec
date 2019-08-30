# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0051_auto_20190724_1335'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitorComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('about', models.CharField(max_length=50, choices=[('OBJECTIVES', 'Objetivos'), ('PICOC', 'PICOC'), ('QUESTIONS', 'Quest\xf5es de Pesquisa'), ('KEYWORDS', 'Palavras-chaves e Sin\xf4nimos'), ('SEARCH_STRING', 'String de Busca'), ('SOURCES', 'Fontes'), ('CRITERIA', 'Crit\xe9rios de Sele\xe7\xe3o'), ('QA_QUESTIONS', 'Quality Assessment Checklist Questions'), ('QA_ANSWERS', 'Quality Assessment Checklist Answers'), ('QA_SCORES', 'Quality Assessment Checklist Scores'), ('RISKS', 'Risks to Review Validity'), ('DATA_EXTRACTION_FORM', 'Formul\xe1rio de Extra\xe7\xe3o de Dados'), ('STATISTICAL_METHODS', 'M\xe9todos Estat\xedsticos e Conven\xe7\xf5es'), ('CONDUCTING_SEARCH', 'Conducting Search'), ('IMPORT_STUDIES', 'Importar Estudos'), ('STUDY_SELECTION', 'Sele\xe7\xe3o de Estudos'), ('QUALITY_ASSESSMENT', 'Avalia\xe7\xe3o de Qualidade'), ('DATA_EXTRACTION', 'Extra\xe7\xe3o de Dados'), ('DATA_ANALYSIS', 'An\xe1lise de Dados')])),
                ('comment', models.CharField(max_length=2000)),
            ],
            options={
                'ordering': ('comment',),
                'verbose_name': 'Visitor Comment',
                'verbose_name_plural': 'Visitor Comments',
            },
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(default='U', max_length=1, choices=[('U', 'N\xe3o classificado'), ('W', 'Aguardando'), ('R', 'Rejeitado'), ('A', 'Aceito'), ('D', 'Duplicado'), ('C', 'Conflito')]),
        ),
        migrations.AlterField(
            model_name='articleevaluation',
            name='status',
            field=models.CharField(default='U', max_length=1, choices=[('U', 'N\xe3o classificado'), ('R', 'Rejeitado'), ('A', 'Aceito'), ('D', 'Duplicado')]),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='related_to',
            field=models.CharField(blank=True, max_length=1, choices=[('P', 'Popula\xe7\xe3o'), ('I', 'Interven\xe7\xe3o'), ('C', 'Compara\xe7\xe3o'), ('O', 'Resultados')]),
        ),
        migrations.AlterField(
            model_name='review',
            name='status',
            field=models.CharField(default='U', max_length=1, choices=[('U', 'N\xe3o publicado'), ('P', 'Publicado')]),
        ),
        migrations.AlterField(
            model_name='selectioncriteria',
            name='criteria_type',
            field=models.CharField(max_length=1, choices=[('I', 'Inclus\xe3o'), ('E', 'Exclus\xe3o')]),
        ),
        migrations.AlterField(
            model_name='study',
            name='status',
            field=models.CharField(default='U', max_length=1, choices=[('U', 'N\xe3o classificado'), ('R', 'Rejeitado'), ('A', 'Aceito'), ('D', 'Duplicado')]),
        ),
        migrations.AddField(
            model_name='visitorcomment',
            name='review',
            field=models.ForeignKey(related_name='review_comments', to='reviews.Review'),
        ),
        migrations.AddField(
            model_name='visitorcomment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
