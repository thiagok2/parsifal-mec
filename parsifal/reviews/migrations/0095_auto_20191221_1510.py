# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0094_auto_20191220_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(default='U', max_length=1, choices=[('U', 'Unclassified'), ('W', 'Waiting'), ('R', 'Rejected'), ('A', 'Accepted'), ('D', 'Duplicated'), ('C', 'Conflict')]),
        ),
        migrations.AlterField(
            model_name='articleevaluation',
            name='status',
            field=models.CharField(default='U', max_length=1, choices=[('U', 'Unclassified'), ('R', 'Rejected'), ('A', 'Accepted'), ('D', 'Duplicated')]),
        ),
        migrations.AlterField(
            model_name='dataextractionfield',
            name='field_type',
            field=models.CharField(max_length=1, choices=[(b'B', 'Boolean Field'), (b'S', 'String Field'), (b'F', 'Float Field'), (b'I', 'Integer Field'), (b'D', 'Date Field'), (b'O', 'Select One Field'), (b'M', 'Select Many Field')]),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='related_to',
            field=models.CharField(blank=True, max_length=2, choices=[('P', 'Population'), ('I', 'Intervention'), ('C', 'Comparison'), ('O', 'Outcome'), ('S', 'Study Type'), ('CT', 'Context')]),
        ),
        migrations.AlterField(
            model_name='review',
            name='pico_type',
            field=models.CharField(default=b'PICOC', max_length=200, choices=[(b'PICOC', 'PICOC'), (b'PICOS', 'PICOS'), (b'Free Text', 'Free Text')]),
        ),
        migrations.AlterField(
            model_name='review',
            name='status',
            field=models.CharField(default='U', max_length=1, choices=[('U', 'Unpublished'), ('P', 'Published')]),
        ),
        migrations.AlterField(
            model_name='selectioncriteria',
            name='criteria_type',
            field=models.CharField(max_length=1, choices=[('I', 'Inclusion'), ('E', 'Exclusion')]),
        ),
        migrations.AlterField(
            model_name='study',
            name='status',
            field=models.CharField(default='U', max_length=1, choices=[('U', 'Unclassified'), ('R', 'Rejected'), ('A', 'Accepted'), ('D', 'Duplicated')]),
        ),
        migrations.AlterField(
            model_name='visitorcomment',
            name='about',
            field=models.CharField(max_length=50, choices=[('OBJECTIVES', 'Objectives'), ('PICOC', 'PICOC'), ('QUESTIONS', 'Research Questions'), ('KEYWORDS', 'Keywords and Synonyms'), ('SEARCH_STRING', 'Search String'), ('SOURCES', 'Sources'), ('CRITERIA', 'Selection Criteria'), ('QA_QUESTIONS', 'Quality Assessment Checklist Questions'), ('QA_ANSWERS', 'Quality Assessment Checklist Answers'), ('QA_SCORES', 'Quality Assessment Checklist Scores'), ('RISKS', 'Risks to Review Validity'), ('DATA_EXTRACTION_FORM', 'Data Extraction Form'), ('STATISTICAL_METHODS', 'Statistical Methods and Conventions'), ('CONDUCTING_SEARCH', 'Conducting Search'), ('IMPORT_STUDIES', 'Import Studies'), ('STUDY_SELECTION', 'Study Selection'), ('QUALITY_ASSESSMENT', 'Quality Assessment'), ('DATA_EXTRACTION', 'Data Extraction'), ('DATA_ANALYSIS', 'Data Analysis')]),
        ),
    ]
