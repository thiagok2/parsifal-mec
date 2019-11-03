# coding: utf-8

import datetime

from django.utils import timezone
from django.utils.html import escape
from django.db import models
from django.db.models import Sum, Q
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from parsifal.library.models import Folder, Document

from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as l_

import reversion

from django.contrib.auth.models import User

@reversion.register()
class Source(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = u'Source'
        verbose_name_plural = u'Sources'
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def set_url(self, value):
        if 'http://' not in value and 'https://' not in value and len(value) > 0:
            self.url = u'http://{0}'.format(value)
        else:
            self.url = value

    def get_articles_count(self, review_id):
        articles_count = Article.objects.filter(review__id=review_id, source__id=self.id).count()
        return articles_count
    def get_article_evaluation_count(self, review_id):
        return Article.objects.filter(review__id=review_id, source__id=self.id).exclude(status=Article.UNCLASSIFIED).count()


@reversion.register()
class Review(models.Model):
    UNPUBLISHED = u'U'
    PUBLISHED = u'P'
    REVIEW_STATUS = (
        (UNPUBLISHED, _('Unpublished')),
        (PUBLISHED, _('Published')),
        )

    PICOC = 'PICOC'
    PICOS = 'PICOS'
    FREE_TEXT = 'Free Text'
    PICO_TYPE = (
        (PICOC, _('PICOC')),
        (PICOS, _('PICOS')),
        (FREE_TEXT, _('Free Text')),
        )

    name = models.SlugField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=2000, null=True, blank=True)
    author = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    objective = models.TextField(max_length=1000)
    sources = models.ManyToManyField(Source)
    status = models.CharField(max_length=1, choices=REVIEW_STATUS, default=UNPUBLISHED)
    co_authors = models.ManyToManyField(User, related_name='co_authors')
    visitors = models.ManyToManyField(User, related_name='visitors')
    quality_assessment_cutoff_score = models.FloatField(default=0.0)
    population = models.CharField(max_length=200, blank=True)
    intervention = models.CharField(max_length=200, blank=True)
    comparison = models.CharField(max_length=200, blank=True)
    outcome = models.CharField(max_length=200, blank=True)
    context = models.CharField(max_length=200, blank=True)
    study_type = models.CharField(max_length=200, blank=True)
    pico_type = models.CharField(max_length=200, choices=PICO_TYPE, default=PICOC)
    pico_text = models.CharField(max_length=1000,  blank=True)
    selection_reviewer = models.ForeignKey(User, null=True, related_name='selection_reviewer')
    export_protocol = models.BooleanField(default=False)
    export_dataextraction = models.BooleanField(default=False)
    export_risks = models.BooleanField(default=False)
    export_qualityassessment = models.BooleanField(default=False)
    export_pico = models.BooleanField(default=False)
    is_metaanalysis = models.BooleanField(default=False)

    statistical_methods=models.TextField(max_length=1000,blank=True)

    #protocol_base = models.ForeignKey('self', null=True, related_name='protocol_base')

    class Meta:
        verbose_name = u'Review'
        verbose_name_plural = u'Reviews'
        unique_together = (('name', 'author'),)

    def __unicode__(self):
        return self.name

    def isExtended(self):
        return self.protocol_base is None

    def isPicoc(self):
        return self.pico_type == self.PICOC

    def isPicos(self):
        return self.pico_type == self.PICOS

    def isStudyTypeFree(self):
        return self.pico_type == self.FREE_TEXT

    #def get_protocol_base(self):
    #    return Review.objects.filter(review__id=self.review.id, protocol_base__id=self.id)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('review', args=(str(self.author.username), str(self.name)))

    def get_questions(self):
        return Question.objects.filter(review__id=self.id)

    def get_inclusion_criterias(self):
        return SelectionCriteria.objects.filter(review__id=self.id, criteria_type='I')

    def get_exclusion_criterias(self):
        return SelectionCriteria.objects.filter(review__id=self.id, criteria_type='E')

    def get_keywords(self):
        return Keyword.objects.filter(review__id=self.id, synonym_of=None)

    def get_tags(self):
        return Tag.objects.filter(review__id=self.id)

    def get_risks(self):
        return Risk.objects.filter(review__id=self.id)

    def get_visitors_comments(self, user):
        return VisitorComment.objects.filter(Q(to__in=[user.id, 0]) | Q(user=user), review__id=self.id, parent=None)

    def get_visitors_unseen_comments(self, user):
        comments = self.get_visitors_comments(user)
        return comments.filter(~Q(comment_seencomments__user=user))

    def is_author_or_coauthor(self, user):
        if user.id == self.author.id:
            return True
        for co_author in self.co_authors.all():
            if user.id == co_author.id:
                return True
        return False

    def is_visitors(self, user):
        for visitor in self.visitors.all():
            if user.id == visitor.id:
                return True
        return False

    def get_users_exclude_authors(self):
        all = User.objects.all()
        users = [user for user in all if not self.is_author_or_coauthor(user)]

        return users

    def get_generic_search_string(self):
        try:
            search_string = SearchSession.objects.filter(review__id=self.id, source=None)[:1].get()
        except SearchSession.DoesNotExist:
            search_string = SearchSession(review=self)
        return search_string

    def get_latest_source_search_strings(self):
        return self.searchsession_set.exclude(source=None).order_by('source__name')

    def get_source_articles(self, source_id=None):
        queryset = Article.objects.filter(review__id=self.id).order_by('updated_by')


        if source_id is not None:
            queryset = queryset.filter(source__id=source_id)

        return queryset

    def get_source_articles_count(self, source_id=None):
        queryset = Article.objects.filter(review__id=self.id).order_by('updated_by')

        if source_id is not None:
            queryset = queryset.filter(source__id=source_id)

        return queryset.count()

    def get_duplicate_articles(self):
        articles = Article.objects.filter(review__id=self.id).exclude(status=Article.DUPLICATED).order_by('title')
        grouped_articles = dict()

        for article in articles:
            slug = slugify(article.title)
            if slug not in grouped_articles.keys():
                grouped_articles[slug] = { 'size': 0, 'articles': list() }
            grouped_articles[slug]['size'] += 1
            grouped_articles[slug]['articles'].append(article)

        duplicates = list()
        for slug, data in grouped_articles.iteritems():
            if data['size'] > 1:
                duplicates.append(data['articles'])

        return duplicates

    def get_accepted_articles(self):
        return Article.objects.filter(review__id=self.id, status=Article.ACCEPTED)

    def get_final_selection_articles(self):
        accepted_articles = Article.objects.filter(review__id=self.id, status=Article.ACCEPTED)
        if self.has_quality_assessment_checklist() and self.quality_assessment_cutoff_score > 0.0:
            articles = accepted_articles
            for article in accepted_articles:
                if article.get_score() <= self.quality_assessment_cutoff_score:
                    articles = articles.exclude(id=article.id)
            return articles
        else:
            return accepted_articles

    def has_quality_assessment_checklist(self):
        has_questions = self.qualityquestion_set.exists()
        has_answers = self.qualityanswer_set.exists()
        return has_questions and has_answers

    def get_data_extraction_fields(self):
        return DataExtractionField.objects.filter(review__id=self.id)

    def get_quality_assessment_questions(self):
        return QualityQuestion.objects.filter(review__id=self.id)

    def get_quality_assessment_answers(self):
        return QualityAnswer.objects.filter(review__id=self.id)

    def calculate_quality_assessment_max_score(self):
        try:
            questions = QualityQuestion.objects.filter(review__id=self.id)
            weight_sum_score = 0.0

            if questions:
                for question in questions:
                    higher_weight_answer = QualityAnswer.objects.filter(review__id=self.id, question__id=question.id).order_by('-weight')[:1].get()
                    weight_sum_score = weight_sum_score + higher_weight_answer.weight

                return weight_sum_score
            else:
                return 0.0
        except:
            return 0.0
    def is_pipoc_completed(self):
        return self.population and self.intervention and self.context and self.objective and self.comparison

    def is_statistical_methods(self):
        return self.statistical_methods is not None

    def articles_count(self):
        articles_count = Article.objects.filter(review__id=self.id).count()
        return articles_count

    def articles_accepts_count(self):
        accepts_count = Article.objects.filter(review__id=self.id,status=Article.ACCEPTED).count()
        return accepts_count

    def pico_type_label(self):
        if (self.pico_type == Review.FREE_TEXT):
            return 'Texto Livre'
        else:
            return self.pico_type

    def get_search_setup(self):
        return SearchSetup.objects.filter(review_id=self.id)

@reversion.register()
class SearchSetup(models.Model):
    COHEN = u'COHEN'
    HATTIE = u'HATTIE'
    CONCLUSION_MODELS = (
        (COHEN, _('Cohen')),
        (HATTIE, _('Hattie')),
        )

    review = models.ForeignKey(Review)
    conclusion_model = models.CharField(max_length=10, choices=CONCLUSION_MODELS, default=HATTIE)
    adverse_effect = models.CharField(max_length=150)
    no_effect = models.CharField(max_length=150)
    small_effect = models.CharField(max_length=150)
    intermediate_effect = models.CharField(max_length=150)
    large_effect = models.CharField(max_length=150)
    developmental_effects = models.CharField(max_length=150)
    teacher_effects = models.CharField(max_length=150)
    zone_desired_effects = models.CharField(max_length=150)

    class Meta:
        verbose_name = u'Search Setup'
        verbose_name_plural = u'Search Setups'

    def __unicode__(self):
        return self.conclusion_model

@reversion.register()
class VisitorComment(models.Model):
    OBJECTIVES = u'OBJECTIVES'
    PICOC = u'PICOC'
    QUESTIONS = u'QUESTIONS'
    KEYWORDS = u'KEYWORDS'
    SEARCH_STRING = u'SEARCH_STRING'
    SOURCES = u'SOURCES'
    CRITERIA = u'CRITERIA'
    QA_QUESTIONS = u'QA_QUESTIONS'
    QA_ANSWERS = u'QA_ANSWERS'
    QA_SCORES = u'QA_SCORES'
    RISKS = u'RISKS'
    DATA_EXTRACTION_FORM = u'DATA_EXTRACTION_FORM'
    STATISTICAL_METHODS = u'STATISTICAL_METHODS'
    CONDUCTING_SEARCH = u'CONDUCTING_SEARCH'
    IMPORT_STUDIES = u'IMPORT_STUDIES'
    STUDY_SELECTION = u'STUDY_SELECTION'
    QUALITY_ASSESSMENT = u'QUALITY_ASSESSMENT'
    DATA_EXTRACTION = u'DATA_EXTRACTION'
    DATA_ANALYSIS = u'DATA_ANALYSIS'
    ABOUT_TYPES = (
        (OBJECTIVES, _(u'Objectives')),
        (PICOC, _(u'PICOC')),
        (QUESTIONS, _(u'Research Questions')),
        (KEYWORDS, _(u'Keywords and Synonyms')),
        (SEARCH_STRING, _(u'Search String')),
        (SOURCES, _(u'Sources')),
        (CRITERIA, _(u'Selection Criteria')),
        (QA_QUESTIONS, _(u'Quality Assessment Checklist Questions')),
        (QA_ANSWERS, _(u'Quality Assessment Checklist Answers')),
        (QA_SCORES, _(u'Quality Assessment Checklist Scores')),
        (RISKS, _(u'Risks to Review Validity')),
        (DATA_EXTRACTION_FORM, _(u'Data Extraction Form')),
        (STATISTICAL_METHODS, _(u'Statistical Methods and Conventions')),
        (CONDUCTING_SEARCH, _(u'Conducting Search')),
        (IMPORT_STUDIES, _(u'Import Studies')),
        (STUDY_SELECTION, _(u'Study Selection')),
        (QUALITY_ASSESSMENT, _(u'Quality Assessment')),
        (DATA_EXTRACTION, _(u'Data Extraction')),
        (DATA_ANALYSIS, _(u'Data Analysis')),
        )

    review = models.ForeignKey(Review, related_name='review_comments')
    user = models.ForeignKey(User, null=True)
    about = models.CharField(max_length=50, choices=ABOUT_TYPES)
    comment = models.CharField(max_length=2000)
    to = models.IntegerField(default=0, null=True)
    parent = models.ForeignKey('self', null=True, default=None, related_name='parent_comment')
    date = models.DateTimeField()
    is_open = models.BooleanField(default=True)

    class Meta:
        verbose_name = u'Visitor Comment'
        verbose_name_plural = u'Visitor Comments'
        ordering = ('-date',)

    def __unicode__(self):
        return self.comment

    def get_user_sended_to(self):
        try:
            return User.objects.get(pk=self.to).profile.get_screen_name()
        except:
            return 'Todos'

    def get_children_comments(self):
        return VisitorComment.objects.filter(parent=self.id).order_by('date')
@reversion.register()
class CommentSeen(models.Model):
    review = models.ForeignKey(Review, related_name='review_seencomments')
    comment = models.ForeignKey(VisitorComment, related_name='comment_seencomments')
    user = models.ForeignKey(User, related_name='user_seencomments')

    class Meta:
        verbose_name = u'Comment Seen'
        verbose_name_plural = u'Comments Seen'
        ordering = ('user',)

    def __unicode__(self):
        return self.user

@reversion.register()
class Tag(models.Model):
    review = models.ForeignKey(Review, related_name='review_tags')
    tag = models.CharField(max_length=300)

    class Meta:
        verbose_name = u'Tag'
        verbose_name_plural = u'Tags'
        ordering = ('tag',)

    def __unicode__(self):
        return self.tag
@reversion.register()
class Invite(models.Model):
    review = models.ForeignKey(Review, related_name='review_invites')
    email = models.CharField(max_length=500)
    invite_type = models.CharField(max_length=100)

    class Meta:
        verbose_name = u'Invite'
        verbose_name_plural = u'Invites'
        ordering = ('email',)

    def __unicode__(self):
        return self.email
@reversion.register()
class Question(models.Model):
    review = models.ForeignKey(Review, related_name='research_questions')
    question = models.CharField(max_length=500)
    parent_question = models.ForeignKey('self', null=True, related_name='+')
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = u'Question'
        verbose_name_plural = u'Questions'
        ordering = ('order',)

    def __unicode__(self):
        return self.question

    def get_child_questions(self):
        return Question.objects.filter(parent_question=self)

@reversion.register()
class SelectionCriteria(models.Model):
    INCLUSION = u'I'
    EXCLUSION = u'E'
    SELECTION_TYPES = (
        (INCLUSION, _(u'Inclusion')),
        (EXCLUSION, _(u'Exclusion')),
        )

    review = models.ForeignKey(Review)
    criteria_type = models.CharField(max_length=1, choices=SELECTION_TYPES)
    description = models.CharField(max_length=200)

    class Meta:
        verbose_name = u'Selection Criteria'
        verbose_name_plural = u'Selection Criterias'
        ordering = ('description',)

    def __unicode__(self):
        return self.description

    def save(self, *args, **kwargs):
        self.description = self.description[:200]
        super(SelectionCriteria, self).save(*args, **kwargs)
@reversion.register()
class Risk(models.Model):
    review = models.ForeignKey(Review, related_name='risks_to_review_validity')
    risk = models.CharField(max_length=500)
    public = models.BooleanField(default=False)
    parent_risk = models.ForeignKey('self', null=True, related_name='+')
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = u'Risk'
        verbose_name_plural = u'Risks'
        ordering = ('order',)

    def __unicode__(self):
        return self.risk

    def get_child_risks(self):
        return Risk.objects.filter(parent_risk=self)
@reversion.register()
class SearchSession(models.Model):
    review = models.ForeignKey(Review)
    source = models.ForeignKey(Source, null=True)
    search_string = models.TextField(max_length=10000)
    version = models.IntegerField(default=1)

    def __unicode__(self):
        return self.search_string

    def search_string_as_html(self):
        escaped_string = escape(self.search_string)
        html = escaped_string.replace(' OR ', ' <strong>OR</strong> ').replace(' AND ', ' <strong>AND</strong> ')
        return html


def search_result_file_upload_to(instance, filename):
    return u'reviews/{0}/search_result/'.format(instance.review.pk)
@reversion.register()
class SearchResult(models.Model):
    review = models.ForeignKey(Review)
    source = models.ForeignKey(Source)
    search_session = models.ForeignKey(SearchSession, null=True)
    imported_file = models.FileField(upload_to=search_result_file_upload_to, null=True)
    documents = models.ManyToManyField(Document)

@reversion.register()
class StudySelection(models.Model):
    review = models.ForeignKey(Review)
    user = models.ForeignKey(User, null=True)
    has_finished = models.BooleanField(default=False)

    def __unicode__(self):
        if self.user:
            selection = u'{0}\'s Selection'.format(self.user.username)
        else:
            selection = u'Final Selection'
        return u'{0} ({1})'.format(selection, self.review.title)

@reversion.register()
class Study(models.Model):
    UNCLASSIFIED = u'U'
    REJECTED = u'R'
    ACCEPTED = u'A'
    DUPLICATED = u'D'
    STUDY_STATUS = (
        (UNCLASSIFIED, _('Unclassified')),
        (REJECTED, _('Rejected')),
        (ACCEPTED, _('Accepted')),
        (DUPLICATED, _('Duplicated')),
        )
    study_selection = models.ForeignKey(StudySelection, related_name=u'studies')
    document = models.ForeignKey(Document)
    source = models.ForeignKey(Source, null=True)
    status = models.CharField(max_length=1, choices=STUDY_STATUS, default=UNCLASSIFIED)
    updated_at = models.DateTimeField(auto_now=True)
    comments = models.TextField(max_length=2000, blank=True, null=True)

@reversion.register()
class Article(models.Model):
    UNCLASSIFIED = u'U'
    WAITING = u'W'
    REJECTED = u'R'
    ACCEPTED = u'A'
    DUPLICATED = u'D'
    CONFLICT = u'C'
    ARTICLE_STATUS = (

        (UNCLASSIFIED, _('Unclassified')),
        (WAITING, _('Waiting')),
        (REJECTED, _('Rejected')),
        (ACCEPTED, _('Accepted')),
        (DUPLICATED, _('Duplicated')),
        (CONFLICT, _('Conflict')),

        )

    ARTICLE_FINAL_STATUS = (
        (REJECTED, _('Rejected')),
        (ACCEPTED, _('Accepted')),
        (DUPLICATED, _('Duplicated'))
    )
    review = models.ForeignKey(Review)
    bibtex_key = models.CharField(max_length=100)
    title = models.CharField(max_length=1000, null=True, blank=True)
    author = models.CharField(max_length=1000, null=True, blank=True)
    journal = models.CharField(max_length=1000, null=True, blank=True)
    year = models.CharField(max_length=10, null=True, blank=True)
    source = models.ForeignKey(Source, null=True)
    pages = models.CharField(max_length=20, null=True, blank=True)
    volume = models.CharField(max_length=100, null=True, blank=True)
    abstract = models.TextField(max_length=4000, null=True, blank=True)
    document_type = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=1, choices=ARTICLE_STATUS, default=UNCLASSIFIED)
    #comments = models.TextField(max_length=2000, null=True, blank=True)
    doi = models.CharField(max_length=50, null=True, blank=True)
    url = models.CharField(max_length=500, null=True, blank=True)
    affiliation = models.CharField(max_length=500, null=True, blank=True)
    author_keywords = models.CharField(max_length=500, null=True, blank=True)
    keywords = models.CharField(max_length=500, null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    issn = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    note = models.CharField(max_length=500, null=True, blank=True)
    finished_data_extraction = models.BooleanField(default=False)
    #selection_criteria = models.ForeignKey(SelectionCriteria, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_by = models.ForeignKey(User, null=True, blank=True, related_name='articles_created', on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name='articles_updated', on_delete=models.SET_NULL)
    evaluation_finished_by = models.ForeignKey(User, null=True, blank=True, related_name='articles_resolved', on_delete=models.SET_NULL)
    evaluation_finished = models.BooleanField(default=False)
    evaluation_finished_at = models.DateTimeField(blank=True, null=True)
    has_empirical_data = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __unicode__(self):
        return self.title

    def get_score(self):
        score = QualityAssessment.objects.filter(article__id=self.id).aggregate(Sum('answer__weight'))
        if score['answer__weight__sum'] == None:
            return 0.0
        return score['answer__weight__sum']

    def get_quality_assesment(self):
        quality_assessments = QualityAssessment.objects.filter(article__id=self.id)
        return quality_assessments

    def get_status_html(self):
        label = { Article.UNCLASSIFIED: 'default', Article.WAITING: 'default', Article.REJECTED: 'danger', Article.CONFLICT: 'danger', Article.ACCEPTED: 'success', Article.DUPLICATED: 'warning' }
        return u'<span class="label label-{0}">{1}</span>'.format(label[self.status], self.get_status_display())

    def get_files(self):
        files = ArticleFile.objects.filter(article__id=self.id)
        return files

    def get_evaluations(self):
        evaluations = ArticleEvaluation.objects.filter(article__id=self.id)
        return evaluations

    def get_user_evaluation(self, user_id=None):
        evaluation = ArticleEvaluation.objects.filter(article__id=self.id, user__id=user_id)

       # if evaluation.count() > 0:
        #    evaluation = evaluation[0]['status']
        # evaluation_status = dict(ArticleEvaluation.ARTICLE_STATUS).get(evaluation)

        return evaluation

    def get_document_type(self):
        result = filter(lambda x: x[0].startswith(self.document_type), Document.ENTRY_TYPES)
        return result[0]

    def get_empirical_values(self):
        empirical_values = ArticleEmpiricalData.objects.filter(article__id=self.id)
        return empirical_values

    def build(self, document):
        self.title = document.title
        self.author = document.author
        self.bibtex_key = document.bibtexkey
        self.author = document.bibtexkey
        self.journal = document.journal
        self.year = document.year
        self.pages = document.pages
        self.volume = document.volume
        self.abstract = document.abstract
        self.document_type = document.entry_type
        self.doi = document.doi
        self.issn = document.issn
        self.url = document.url
        self.affiliation = document.institution
        self.publisher = document.publisher
        self.language = document.language
        self.note = document.note
@reversion.register()
class ArticleEmpiricalData(models.Model):
    PRIMARY = u'P'
    EFFECT_SIZE = u'E'
    DATA_TYPES = (
        (PRIMARY, _('Primary data')),
        (EFFECT_SIZE, _('Precalculated Effect Size')),
    )

    article = models.OneToOneField(Article, on_delete=models.CASCADE, primary_key=True)
    data_type = models.CharField(max_length=100, choices=DATA_TYPES, default=PRIMARY)
    n1 = models.IntegerField(null=True, blank=True)
    dp1 = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    a1 = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    n2 = models.IntegerField(null=True, blank=True)
    dp2 = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    a2 = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    effect_size = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    min_limit = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    max_limit = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    std_error = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)

    class Meta:
        verbose_name = u'Article Empirical Data'
        verbose_name_plural = u'Articles Empirical Data'
        ordering = ('article',)

    def __unicode__(self):
        return self.article

def article_directory_path(instance, filename):
    return 'article/{0}/{1}'.format(instance.article.id, filename)
@reversion.register()
class ArticleFile(models.Model):
    review = models.ForeignKey(Review, related_name='file_review')
    article = models.ForeignKey(Article, related_name='file_article')
    user = models.ForeignKey(User, related_name='file_user')
    article_file = models.FileField(upload_to=article_directory_path)
    name = models.CharField(max_length=300)
    size = models.CharField(max_length=150)
@reversion.register()
class ArticleEvaluation(models.Model):
    UNCLASSIFIED = u'U'
    REJECTED = u'R'
    ACCEPTED = u'A'
    DUPLICATED = u'D'
    ARTICLE_STATUS = (
        (UNCLASSIFIED, _('Unclassified')),
        (REJECTED, _('Rejected')),
        (ACCEPTED, _('Accepted')),
        (DUPLICATED, _('Duplicated')),
        )

    review = models.ForeignKey(Review, related_name='evaluation_review')
    article = models.ForeignKey(Article, related_name='evaluation_article')
    user = models.ForeignKey(User, related_name='evaluation_user')
    selection_criteria = models.ForeignKey(SelectionCriteria, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=1, choices=ARTICLE_STATUS, default=UNCLASSIFIED)
    comments = models.TextField(max_length=2000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = u'ArticleEvaluation'
        verbose_name_plural = u'ArticleEvaluations'
        ordering = ('status',)
        unique_together = (("review", "article", "user"),)

    def __unicode__(self):
        return self.user.username+' - '+self.status

    def get_status_html(self):
        label = { ArticleEvaluation.UNCLASSIFIED: 'default', ArticleEvaluation.REJECTED: 'danger', ArticleEvaluation.ACCEPTED: 'success', ArticleEvaluation.DUPLICATED: 'warning' }
        return u'<span class="label label-{0}">{1}</span>'.format(label[self.status], self.get_status_display())
@reversion.register()
class Keyword(models.Model):
    POPULATION = u'P'
    INTERVENTION = u'I'
    COMPARISON = u'C'
    OUTCOME = u'O'
    STUDY_TYPE = u'S'
    CONTEXT = u'CT'
    RELATED_TO = (
        (POPULATION, _('Population')),
        (INTERVENTION, _('Intervention')),
        (COMPARISON, _('Comparison')),
        (OUTCOME, _('Outcome')),
        (STUDY_TYPE, _('Study Type')),
        (CONTEXT, _('Context')),
        )

    review = models.ForeignKey(Review, related_name='keywords')
    description = models.CharField(max_length=200)
    synonym_of = models.ForeignKey('self', null=True, related_name='synonyms')
    related_to = models.CharField(max_length=1, choices=RELATED_TO, blank=True)

    class Meta:
        verbose_name = u'Keyword'
        verbose_name_plural = u'Keywords'
        ordering = ('description',)

    def __unicode__(self):
        return self.description

    def save(self, *args, **kwargs):
        self.description = self.description[:200]
        super(Keyword, self).save(*args, **kwargs)

    def get_synonyms(self):
        return Keyword.objects.filter(review__id=self.review.id, synonym_of__id=self.id)
@reversion.register()
class QualityQuestion(models.Model):
    review = models.ForeignKey(Review)
    description = models.CharField(max_length=255)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Quality Assessment Question'
        verbose_name_plural = 'Quality Assessment Questions'
        ordering = ('order',)

    def __unicode__(self):
        return self.description

    def get_answers(self):
        return QualityAnswer.objects.filter(question__id=self.id, review__id=self.review.id)
@reversion.register()
class QualityAnswer(models.Model):
    SUGGESTED_ANSWERS = (
        (_('Yes'), 1.0),
        (_('Partially'), 0.5),
        (_('No'), 0.0)
        )

    review = models.ForeignKey(Review)
    question = models.ForeignKey(QualityQuestion)
    description = models.CharField(max_length=255)
    weight = models.FloatField()

    class Meta:
        verbose_name = 'Quality Assessment Answer'
        verbose_name_plural = 'Quality Assessment Answers'
        ordering = ('-weight',)

    def __unicode__(self):
        return self.description
@reversion.register()
class QualityAssessment(models.Model):
    user = models.ForeignKey(User, null=True)
    article = models.ForeignKey(Article)
    question = models.ForeignKey(QualityQuestion)
    answer = models.ForeignKey(QualityAnswer, null=True)

    def __unicode__(self):
        return str(self.article.id) + ' ' + str(self.question.id)


@reversion.register()
class DataExtractionField(models.Model):
    BOOLEAN_FIELD = 'B'
    STRING_FIELD = 'S'
    FLOAT_FIELD = 'F'
    INTEGER_FIELD = 'I'
    DATE_FIELD = 'D'
    SELECT_ONE_FIELD = 'O'
    SELECT_MANY_FIELD = 'M'
    FIELD_TYPES = (
        (BOOLEAN_FIELD, _('Boolean Field')),
        (STRING_FIELD, _('String Field')),
        (FLOAT_FIELD, _('Float Field')),
        (INTEGER_FIELD, _('Integer Field')),
        (DATE_FIELD, _('Date Field')),
        (SELECT_ONE_FIELD, _('Select One Field')),
        (SELECT_MANY_FIELD, _('Select Many Field')),
        )

    review = models.ForeignKey(Review)
    description = models.CharField(max_length=255)
    field_type = models.CharField(max_length=1, choices=FIELD_TYPES)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Data Extraction Field'
        verbose_name_plural = 'Data Extraction Fields'
        ordering = ('order',)

    def get_select_values(self):
        return DataExtractionLookup.objects.filter(field__id=self.id)

    def is_select_field(self):
        return self.field_type in (self.SELECT_ONE_FIELD, self.SELECT_MANY_FIELD)

@reversion.register()
class DataExtractionLookup(models.Model):
    field = models.ForeignKey(DataExtractionField)
    value = models.CharField(max_length=1000)

    class Meta:
        verbose_name = 'Lookup Value'
        verbose_name_plural = 'Lookup Values'
        ordering = ('value',)

    def __unicode__(self):
        return self.value

@reversion.register()
class DataExtraction(models.Model):
    user = models.ForeignKey(User, null=True)
    article = models.ForeignKey(Article)
    field = models.ForeignKey(DataExtractionField)
    value = models.TextField(blank=True, null=True)
    select_values = models.ManyToManyField(DataExtractionLookup)

    def _set_boolean_value(self, value):
        if value:
            if value in ['True', 'False']:
                self.value = value
            else:
                raise ValueError(_('Expected values: "True" or "False"'))
        else:
            self.value = ''

    def _set_string_value(self, value):
        try:
            self.value = value.strip()
        except Exception, e:
            raise e

    def _set_float_value(self, value):
        try:
            if value:
                _value = value.replace(',', '.')
                self.value = float(_value)
            else:
                self.value = ''
        except:
            raise Exception(_('Invalid input for ') + self.field.description + _(' field. Expected value: floating point number. Please use dot instead of comma.'))

    def _set_integer_value(self, value):
        try:
            if value:
                _value = value.replace(',', '.')
                self.value = int(float(_value))
            else:
                self.value = ''
        except:
            raise Exception(_('Invalid input for ') + self.field.description + _(' field. Expected value: integer number.'))

    def _set_date_value(self, value):
        try:
            if value:
                _value = datetime.datetime.strptime(value, '%m/%d/%Y').date()
                self.value = str(_value)
            else:
                self.value = ''
        except:
            raise Exception(_('Invalid input for ') + self.field.description + _(' field. Expected value: date. Please use the format MM/DD/YYYY.'))

    def _set_select_one_value(self, value):
        try:
            self.value = ''
            self.select_values.clear()
            if value:
                _value = DataExtractionLookup.objects.get(pk=value)
                self.select_values.add(_value)
        except Exception, e:
            raise e

    def _set_select_many_value(self, value):
        try:
            self.value = ''
            _value = DataExtractionLookup.objects.get(pk=value)
            if _value in self.select_values.all():
                self.select_values.remove(_value)
            else:
                self.select_values.add(_value)
        except Exception, e:
            raise e

    def set_value(self, value):
        set_value_functions = {
            DataExtractionField.BOOLEAN_FIELD: self._set_boolean_value,
            DataExtractionField.STRING_FIELD: self._set_string_value,
            DataExtractionField.FLOAT_FIELD: self._set_float_value,
            DataExtractionField.INTEGER_FIELD: self._set_integer_value,
            DataExtractionField.DATE_FIELD: self._set_date_value,
            DataExtractionField.SELECT_ONE_FIELD: self._set_select_one_value,
            DataExtractionField.SELECT_MANY_FIELD: self._set_select_many_value,
        }
        set_value_functions[self.field.field_type](value[:1000])

    def _get_boolean_value(self):
        try:
            if self.value == 'True':
                return True
            elif self.value == 'False':
                return False
            else:
                return ''
        except Exception, e:
            return ''

    def _get_string_value(self):
        return self.value

    def _get_float_value(self):
        try:
            return float(self.value)
        except Exception, e:
            return ''

    def _get_integer_value(self):
        try:
            return int(self.value)
        except Exception, e:
            return ''

    def _get_date_value(self):
        try:
            if self.value != '':
                return datetime.datetime.strptime(self.value, '%Y-%m-%d').date()
            else:
                return ''
        except Exception, e:
            return ''

    def _get_select_one_value(self):
        try:
            return self.select_values.all()[0]
        except Exception, e:
            return None

    def _get_select_many_value(self):
        try:
            return self.select_values.all()
        except Exception, e:
            return []

    def get_value(self):
        if self.field.field_type:
            get_value_functions = {
                DataExtractionField.BOOLEAN_FIELD: self._get_boolean_value,
                DataExtractionField.STRING_FIELD: self._get_string_value,
                DataExtractionField.FLOAT_FIELD: self._get_float_value,
                DataExtractionField.INTEGER_FIELD: self._get_integer_value,
                DataExtractionField.DATE_FIELD: self._get_date_value,
                DataExtractionField.SELECT_ONE_FIELD: self._get_select_one_value,
                DataExtractionField.SELECT_MANY_FIELD: self._get_select_many_value,
            }
            return get_value_functions[self.field.field_type]()
        return self._get_string_value()

    def get_date_value_as_string(self):
        try:
            value = self.get_value()
            return value.strftime('%m/%d/%Y')
        except Exception, e:
            return ''
