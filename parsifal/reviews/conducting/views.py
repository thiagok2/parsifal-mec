# coding: utf-8

import json
import os
from os.path import splitext
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
import xlwt

from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse as r
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, get_object_or_404, render
from django.template import RequestContext
from django.conf import settings as django_settings
from django.core.context_processors import csrf
from django.db.models import Count, Sum
from django.utils.html import escape
from numpy import *

from parsifal.reviews.models import *
from parsifal.reviews.forms import ArticleUploadForm
from parsifal.reviews.decorators import main_author_required, author_required, author_or_visitor_required
from parsifal.utils.elsevier.client import ElsevierClient
from parsifal.utils.elsevier.exceptions import *
from django.template.loader import render_to_string

from django.utils.translation import ugettext as _

from parsifal.reviews.conducting.forms import FolderForm, DocumentForm, SharedFolderForm
from parsifal.reviews.models import Article, Source, Review
import math
from parsifal.utils.meta_analysis import cohen_d, effect_size_comb,\
    cin_efs_lower_limit, cin_efs_max_limit
import requests
from decouple import config
from django.template.defaultfilters import nan

@author_or_visitor_required
@login_required
def conducting(request, username, review_name):
    return redirect(r('search_studies', args=(username, review_name)))

@author_or_visitor_required
@login_required
def search_studies(request, username, review_name):
    review = get_object_or_404(Review, name=review_name, author__username__iexact=username)
    unseen_comments = review.get_visitors_unseen_comments(request.user)
    sessions = review.get_latest_source_search_strings()
    add_sources = review.sources.exclude(id__in=sessions.values('source__id'))
    database_queries = {}
    try:
        scopus = sessions.filter(source__name__iexact='Scopus')[0]
        database_queries['scopus'] = scopus
    except:
        pass
    try:
        science_direct = sessions.filter(source__name__iexact='Science@Direct')[0]
        database_queries['science_direct'] = science_direct
    except:
        pass
    sources_names = []
    for source in review.sources.all():
        sources_names.append(source.name.lower())
    return render(request, 'conducting/conducting_search_studies.html', {
            'review': review,
            'add_sources': add_sources,
            'database_queries': database_queries,
            'sources_names': sources_names,
            'unseen_comments': unseen_comments
            })

@author_required
@login_required
@require_POST
def save_source_string(request):
    try:
        review_id = request.POST.get('review-id')
        source_id = request.POST.get('source-id')
        review = Review.objects.get(pk=review_id)
        source = Source.objects.get(pk=source_id)
        search_string = request.POST.get('search_string')
        try:
            search_session = review.get_latest_source_search_strings().get(source=source)
        except SearchSession.DoesNotExist:
            search_session = SearchSession(review=review, source=source)
        search_session.search_string = search_string
        search_session.save()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()

@author_required
@login_required
@require_POST
def remove_source_string(request):
    try:
        review_id = request.POST.get('review-id')
        source_id = request.POST.get('source-id')
        review = Review.objects.get(pk=review_id)
        source = Source.objects.get(pk=source_id)
        search_string = request.POST.get('search_string')
        try:
            search_session = review.get_latest_source_search_strings().get(source=source)
            search_session.delete()
        except SearchSession.DoesNotExist:
            pass
        messages.success(request, _('{0} search string removed successfully!').format(source.name))
    except:
        messages.error(request, _('{0} search string removed successfully!').format(source.name))
    return redirect(r('search_studies', args=(review.author.username, review.name)))

@author_required
@login_required
@require_POST
def import_base_string(request):
    try:
        review_id = request.POST.get('review-id')
        source_id = request.POST.get('source-id')
        review = Review.objects.get(pk=review_id)
        source = Source.objects.get(pk=source_id)
        base_search_string = review.get_generic_search_string().search_string
        try:
            search_session = review.get_latest_source_search_strings().get(source=source)
        except SearchSession.DoesNotExist:
            search_session = SearchSession(review=review, source=source)
        search_session.search_string = base_search_string
        search_session.save()
        return HttpResponse(base_search_string)
    except:
        return HttpResponseBadRequest()

def elsevier_search(request, database):
    client = ElsevierClient(django_settings.ELSEVIER_API_KEY)
    query = request.GET.get('query', '')
    query = ' '.join(query.split())
    count = request.GET.get('count', '25')
    start = request.GET.get('start', '0')
    try:
        result = {}
        if database == 'scopus':
            result = client.search_scopus({ 'query': query, 'count': count, 'start': start })
        elif database == 'science_direct':
            result = client.search_science_direct({ 'query': query, 'count': count, 'start': start })
        data = json.dumps(result)
        return HttpResponse(data, content_type='application/json')
    except ElsevierInvalidRequest, e:
        return HttpResponseBadRequest(_('Invalid query. Please verify the syntax of your query before executing a new search.'))
    except ElsevierQuotaExceeded, e:
        return HttpResponseBadRequest(_('Parsifal\'s search quota on Elsevier\'s databases exceeded. Please try again later.'))


@author_required
@login_required
def search_scopus(request):
    return elsevier_search(request, 'scopus')

@author_required
@login_required
def search_science_direct(request):
    return elsevier_search(request, 'science_direct')

@author_or_visitor_required
@login_required
def import_studies(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username__iexact=username)
    unseen_comments = review.get_visitors_unseen_comments(request.user)
    sources = []
    for source in review.sources.all():
        sources.append({
            'source': source,
            'count': Article.objects.filter(source=source, review=review).count()
            })
    return render(request, 'conducting/conducting_import_studies.html', {
            'review': review,
            'sources': sources,
            'unseen_comments': unseen_comments
        })

@author_or_visitor_required
@login_required
def study_selection(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username__iexact=username)
    unseen_comments = review.get_visitors_unseen_comments(request.user)
    try:
        active_tab = int(request.GET['source'])
    except Exception, e:
        active_tab = -1

    add_sources = review.sources.count()
    import_articles = review.get_source_articles().count()

    steps_messages = []
    if not add_sources: steps_messages.append(u'Use the <a href="{0}#sources-section">planning tab</a> to add sources to your review.'.format(r('protocol', args=(username, review_name))))
    if not import_articles: steps_messages.append(_('Import the studies using the') + '<a href="{0}">'.format(r('import_studies', args=(username, review_name))) + _('import studies tab') +'</a>.')

    finished_all_steps = len(steps_messages) == 0

    return render(request, 'conducting/conducting_study_selection.html', {
            'review': review,
            'active_tab': active_tab,
            'steps_messages': steps_messages,
            'finished_all_steps': finished_all_steps,
            'unseen_comments': unseen_comments
        })

def update_article_empirical_data(request):
    try:
        article_id = request.GET['article-id']
        has_empirical_data = request.GET['has-empirical-data']

        if article_id:
            article = Article.objects.get(pk=article_id)
            article.has_empirical_data = True if has_empirical_data == 'true' else False
            article.save()

            if has_empirical_data == 'false':
                empirical_data = ArticleEmpiricalData.objects.get(pk=article_id).delete()

        context = RequestContext(request, {'article': article, 'user': request.user})
        return render_to_response('conducting/partial_conducting_article_row.html', context)
    except:
        return HttpResponseBadRequest()

def build_quality_assessment_table(request, review, order):
    selected_studies = review.get_accepted_articles().annotate(sum=Sum('qualityassessment__answer__weight')).order_by(order)
    quality_questions = QualityQuestion.objects.filter(review__id=review.id)

    if quality_questions:
        str_table = u''
        for study in selected_studies:
            str_table += u'''
            <div class="panel panel-default panel-quality-assessment">
              <div class="panel-heading">
                <h3 class="panel-title">{0} <br/><small> {5}, ({4})</small><span class="badge score pull-right">{1}</span></h3>
              </div>

            <table class="table" id="tbl-quality" article-id="{2}" csrf-token="{3}">
                <tbody>'''.format(escape(study.title), study.get_score(), study.id, unicode(csrf(request)['csrf_token']), escape(study.year), escape(study.author))

            quality_assessment = study.get_quality_assesment()

            for question in quality_questions:
                quality_answers = question.get_answers()
                str_table += u'''<tr question-id="''' + str(question.id) + '''">
                <td>''' + escape(question.description) + '''</td>'''

                try:
                    question_answer = quality_assessment.filter(question__id=question.id).get()
                except:
                    question_answer = None

                for answer in quality_answers:
                    selected_answer = ''
                    if question_answer is not None:
                        if answer.id == question_answer.answer.id:
                            selected_answer = ' selected-answer'
                    str_table += u'''<td class="answer'''+ selected_answer +'''" answer-id="''' + str(answer.id) + '''">''' + escape(answer.description) + '''</td>'''
                str_table += u'''</tr>'''

            str_table += u'''</tbody></table></div>'''
        return str_table
    else:
        return ''

@author_or_visitor_required
@login_required
def quality_assessment(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username__iexact=username)
    unseen_comments = review.get_visitors_unseen_comments(request.user)

    add_sources = review.sources.count()
    import_articles = review.get_source_articles().count()
    select_articles = review.get_accepted_articles().count()
    create_questions = review.get_quality_assessment_questions().count()
    create_answers = review.get_quality_assessment_answers().count()

    steps_messages = []

    if not add_sources: steps_messages.append(_('Use the <a href="/')+ username +'/'+ review_name +'/planning/protocol/#sources-section">planning tab</a> to add sources to your review.')
    if not import_articles: steps_messages.append(_('Import the studies using the <a href="/')+ username +'/'+ review_name +'/conducting/import/">import studies tab</a>.')
    if not select_articles: steps_messages.append(_('Classify the imported studies using the <a href="/')+ username +'/'+ review_name +'/conducting/studies/">study selection tab</a>.')
    if not create_questions: steps_messages.append(_('Create quality assessment questions using the <a href="/')+ username +'/'+ review_name +'/planning/quality/#questions">planning tab</a>.')
    if not create_answers: steps_messages.append(_('Create quality assessment answers using the <a href="/')+ username +'/'+ review_name +'/planning/quality/#answers">planning tab</a>.')

    finished_all_steps = len(steps_messages) == 0

    order = 'title'
    if 'order' in request.GET:
        order = request.GET.get('order')
    elif 'quality_assessment_order' in request.session:
        order = request.session.get('quality_assessment_order')
    if order not in ('title', '-title', 'year', '-year', 'sum', '-sum'):
        order = 'title'
    request.session['quality_assessment_order'] = order

    quality_assessment_table = build_quality_assessment_table(request, review, order)

    return render(request, 'conducting/conducting_quality_assessment.html', {
            'review': review,
            'steps_messages': steps_messages,
            'quality_assessment_table': quality_assessment_table,
            'finished_all_steps': finished_all_steps,
            'order': order,
            'unseen_comments': unseen_comments
        })

def build_data_extraction_field_row(article, field):
    str_field = u''

    try:
        extraction = DataExtraction.objects.get(article=article, field=field)
    except Exception, e:
        extraction = None

    if field.field_type == DataExtractionField.BOOLEAN_FIELD:
        true = u''
        false = u''
        if extraction != None:
            if extraction.get_value() == True:
                true = u' selected'
            elif extraction.get_value() == False:
                false = u' selected'

        str_field = u'''<select name="value" class="form-control">
            <option value="">Selecione...</option>
            <option value="True"{0}>Verdadeiro</option>
            <option value="False"{1}>Falso</option>
          </select>'''.format(true, false)

    elif field.field_type == DataExtractionField.DATE_FIELD:
        if extraction != None:
            value = extraction.get_date_value_as_string()
        else:
            value = u''
        str_field = u'<input type="text" class="form-control" name="{0}-{1}-value" maxlength="10" value="{2}">'.format(article.id, field.id, escape(value))

    elif field.field_type == DataExtractionField.SELECT_ONE_FIELD:
        str_field = u'''<select name="{0}-{1}-value" class="form-control">
            <option value="">Selecione...</option>'''.format(article.id, field.id)
        for value in field.get_select_values():
            if extraction != None and extraction.get_value() != None and extraction.get_value().id == value.id:
                selected = ' selected'
            else:
                selected = ''
            str_field += u'''<option value="{0}"{1}>{2}</option>'''.format(value.id, selected, escape(value.value))
        str_field += u'</select>'

    elif field.field_type == DataExtractionField.SELECT_MANY_FIELD:
        for value in field.get_select_values():
            if extraction != None and value in extraction.get_value():
                checked = ' checked'
            else:
                checked = ''
            str_field += u'<label class="checkbox-inline"><input type="checkbox" name="{0}-{1}-value" value="{2}"{3}>{4}</label> '.format(article.id, field.id, value.id, checked, escape(value.value))

    elif field.field_type == DataExtractionField.STRING_FIELD:
        value = ''
        if extraction != None:
            value = extraction.get_value()
        str_field = u'<textarea class="form-control" name="{0}-{1}-value" rows="3">{2}</textarea>'.format(article.id, field.id, escape(value))
    else:
        value = ''
        if extraction != None:
            value = extraction.get_value()
        str_field = u'<input type="text" class="form-control" maxlength="30" name="{0}-{1}-value" value="{2}">'.format(article.id, field.id, escape(value))

    return str_field

def build_data_extraction_table(review, is_finished):
    selected_studies = review.get_final_selection_articles()
    if is_finished != None:
        selected_studies = selected_studies.filter(finished_data_extraction=is_finished)
    data_extraction_fields = review.get_data_extraction_fields()
    has_quality_assessment = review.has_quality_assessment_checklist()
    if selected_studies and data_extraction_fields:
        str_table = u'<div class="panel-group">'
        for study in selected_studies:
            #if has_quality_assessment:
            str_table += u'''<div class="panel panel-default data-extraction-panel">
              <div class="panel-heading">
                <h3 class="panel-title row">
                   <div class="col-sm-9 article-container" style="padding: 0px 5px">
                   <span id="title-study-{2}">{0}</span>
                  <span class="badge">{1}</span>'''.format(escape(study.title), study.get_score(), study.id)

            files = study.get_files();
            if files:
                pdf_file = files[0]
                str_table +='''<a href="{0}" target="_blank"><span class="badge" ><i class="glyphicon glyphicon-cloud-download"></i></span></a>'''.format(pdf_file.article_file.url)
            if study.doi:
                str_table +='''<a href="https://dx.doi.org/{0}" target="blank"><span class="badge">DOI:{0}</a>'''.format(study.doi,study.doi)


            str_table +='''<a href="#" oid="{0}" class="article-link"><span class="badge" ><i class="glyphicon glyphicon-edit"></i></span></a>'''.format(study.id)

            str_table +=u'''<div class="detail-article-data-extraction">
                            <small><span id="subtitle-study-{2}" class="text-muted">{0} ({1})</span></small>
                        </div>'''.format(escape(study.author), study.year, study.id)

            str_table +='</div>'
            str_table += u'</h3></div>'
            str_table += u'<div class="panel-body form-horizontal" data-article-id="{0}">'.format(study.id)
            #else:
            #    str_table += u'''<div class="panel panel-default data-extraction-panel">
            #      <div class="panel-heading">
            #        <h3 class="panel-title">{1}</h3>
            #      </div>
            #      <div class="panel-body form-horizontal" data-article-id="{0}">'''.format(study.id, escape(study.title))

            for field in data_extraction_fields:
                str_table += u'''<div class="form-group" data-field-id="{0}">
                    <label class="control-label col-md-2">{1}</label>
                    <div class="col-md-10">{2}<span class="help-block error" style="display: none;"></span>
                    </div>
                </div>
                '''.format(field.id, escape(field.description), build_data_extraction_field_row(study, field))

            if study.has_empirical_data:
                checked = 'checked'
                hide = ''
            else:
                checked = ''
                hide = 'hide'
            if review.is_metaanalysis:
                str_table += u'''<div class="form-group">
                        <label class="control-label col-md-2">Possui dados empíricos?</label>
                        <div class="col-md-10" style="padding-top:7px;">
                            <input type="checkbox" id="ck-empirical-data" {0} />
                        </div>
                    </div>
                    '''.format(checked)


                empirical_values, created = ArticleEmpiricalData.objects.get_or_create(article=study)
                empirical_values.save()

                if empirical_values:
                    empirical_values.n1 = empirical_values.n1 if empirical_values.n1 != None else ''
                    empirical_values.dp1 = empirical_values.dp1 if empirical_values.dp1 != None else ''
                    empirical_values.a1 = empirical_values.a1 if empirical_values.a1 != None else ''
                    empirical_values.n2 = empirical_values.n2 if empirical_values.n2 != None else ''
                    empirical_values.dp2 = empirical_values.dp2 if empirical_values.dp2 != None else ''
                    empirical_values.a2 = empirical_values.a2 if empirical_values.a2 != None else ''
                    empirical_values.effect_size = empirical_values.effect_size if empirical_values.effect_size != None else ''
                    empirical_values.min_limit = empirical_values.min_limit if empirical_values.min_limit != None else ''
                    empirical_values.max_limit = empirical_values.max_limit if empirical_values.max_limit != None else ''
                    empirical_values.std_error = empirical_values.std_error if empirical_values.std_error != None else ''

                str_table += u'''<form class="{1}" name="empirical-values-{0}" id="empirical-values-{0}" method="get" action=".">
                        <div class="form-group">
                            <span class="col-sm-offset-2 col-sm-8 error alert alert-danger" style="display: none;"></span>
                            <div class="row">
                                <div class="col-md-12">
                                <label class="control-label col-md-2">Data type</label>
                                    <div class="col-md-3" style="padding-top:7px;">
                                        <select name="data-type" id="empirical-data-type-{0}" data-empirical class="form-control">'''.format(study.id, hide)

                for data_type in empirical_values.DATA_TYPES:
                    selected = 'selected' if empirical_values.data_type == data_type[0] else ''
                    str_table += u'''<option value="{1}" {3}>{2}</option>'''.format(study.id, data_type[0], data_type[1], selected)

                str_table += u'''</select>
                                </div>
                            </div>
                        </div>
                    </div>
                        '''

                hide_primary = 'hide' if empirical_values.data_type == 'E' else ''
                hide_effect = 'hide' if empirical_values.data_type == 'P' else ''

                str_table += u'''<div class="form-group">
                            <input type="hidden" name="article-id" id="article-id" value="{0}">
                            <input type="hidden" name="review-id" id="review-id" value="{2}">
                            <div id="primary-data-{0}" class="{4}">
                                <div class="row">
                                    <div class="col-md-12">
                                        <label class="control-label col-md-2">N¹</label>
                                        <div class="col-md-2" style="padding-top:7px;">
                                            <input type="text" class="form-control" value="{3.n1}" name="n1" id="{0}-n1-value" data-empirical data-type="n1"/>
                                        </div>
                                        <label class="control-label col-md-1">DP¹</label>
                                        <div class="col-md-2" style="padding-top:7px;">
                                            <input type="text" class="form-control" value="{3.dp1}" name="dp1" id="{0}-dp1-value" data-empirical data-type="dp1" />
                                        </div>
                                        <label class="control-label col-md-1">A¹</label>
                                        <div class="col-md-2" style="padding-top:7px;">
                                            <input type="text" class="form-control" value="{3.a1}" name="a1" id="{0}-a1-value" data-empirical data-type="a1"/>
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-12">
                                        <label class="control-label col-md-2">N²</label>
                                        <div class="col-md-2" style="padding-top:7px;">
                                            <input type="text" class="form-control" value="{3.n2}" name="n2" id="{0}-n2-value" data-empirical data-type="n2" />
                                        </div>
                                        <label class="control-label col-md-1">DP²</label>
                                        <div class="col-md-2" style="padding-top:7px;">
                                            <input type="text" class="form-control" value="{3.dp2}" name="dp2" id="{0}-dp2-value" data-empirical data-type="dp2" />
                                        </div>
                                        <label class="control-label col-md-1">A²</label>
                                        <div class="col-md-2" style="padding-top:7px;">
                                            <input type="text" class="form-control" value="{3.a2}" name="a2" id="{0}-a2-value" data-empirical data-type="a2" />
                                        </div>
                                    </div>
                                    <div class="col-md-12 text-center" style="padding: 15px; color: #444">
                                        <small>(¹ ⇒ Treatment group | ² ⇒ Control group) | N ⇒ Sample Size | A ⇒ Average</small>
                                    </div>
                                </div>
                            </div>
                            <div id="effect-data-{0}" class="{5}">
                                <div class="row">
                                    <div class="col-md-12">
                                        <label class="control-label col-md-2">Effect Size</label>
                                        <div class="col-md-2" style="padding-top:7px;">
                                            <input type="text" class="form-control" value="{3.effect_size}" name="effect-size" id="{0}-effect-size-value" data-empirical data-type="effect-size"/>
                                        </div>
                                        <label class="control-label col-md-1">Lower Limit</label>
                                        <div class="col-md-2" style="padding-top:7px;">
                                            <input type="text" class="form-control" value="{3.min_limit}" name="min-limit" id="{0}-min-limit-value" data-empirical data-type="min-limit" />
                                        </div>
                                        <label class="control-label col-md-1">Upper Limit</label>
                                        <div class="col-md-2" style="padding-top:7px;">
                                            <input type="text" class="form-control" value="{3.max_limit}" name="max-limit" id="{0}-max-limit-value" data-empirical data-type="max-limit"/>
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-12">
                                        <label class="control-label col-md-2">Standard error</label>
                                        <div class="col-md-2" style="padding-top:7px;padding-bottom: 15px;">
                                            <input type="text" class="form-control" value="{3.std_error}" name="std-error" id="{0}-std-error-value" data-empirical data-type="std-error"/>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                    '''.format(study.id, hide, review.id, empirical_values, hide_primary, hide_effect)

            if study.finished_data_extraction:
                str_table += u'<div class="col-sm-offset-2 col-sm-3"><span class=""><a href="javascript:void(0);" class="js-finished-button btn btn-success js-mark-as-not-finished"><span class="action-text">Marcar como não resolvido</span></a></span></div>'
            else:
                str_table += u'<div class="col-sm-offset-2 col-sm-3"><span class=""><a href="javascript:void(0);" class="js-finished-button btn btn-success js-mark-as-finished"><span class="action-text">Marcar como resolvido</span></a></span></div>'

            str_table += u'</div></div>'
        str_table += "</div>"
        return str_table
    else:
        return u''

@author_or_visitor_required
@login_required
def data_extraction(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username__iexact=username)
    unseen_comments = review.get_visitors_unseen_comments(request.user)

    add_sources = review.sources.count()
    import_articles = review.get_source_articles().count()
    select_articles = review.get_accepted_articles().count()
    create_fields = review.get_data_extraction_fields().count()

    steps_messages = []

    if not add_sources: steps_messages.append(_('Use the <a href="/')+ username +'/'+ review_name +'/planning/protocol/#sources-section">planning tab</a> to add sources to your review.')
    if not import_articles: steps_messages.append(_('Import the studies using the <a href="/')+ username +'/'+ review_name +'/conducting/import/">import studies tab</a>.')
    if not select_articles: steps_messages.append(_('Classify the imported studies using the <a href="/')+ username +'/'+ review_name +'/conducting/studies/">study selection tab</a>.')
    if not create_fields: steps_messages.append(_('Create data extraction fields using the <a href="/')+ username +'/'+ review_name +'/planning/extraction/">planning tab</a>.')

    finished_all_steps = not steps_messages

    tab = request.GET.get('tab', 'todo')
    if tab not in ['todo', 'done', 'all']:
        tab = 'todo'

    is_finished = None

    if tab == 'todo':
        is_finished = False
    elif tab == 'done':
        is_finished = True
    elif tab == 'all':
        is_finished = None

    try:
        data_extraction_table = build_data_extraction_table(review, is_finished)
    except Exception, e:
        raise e
        data_extraction_table = _('<h3>Something went wrong while rendering the data extraction form.</h3>')

    return render(request, 'conducting/conducting_data_extraction.html', {
            'review': review,
            'steps_messages': steps_messages,
            'data_extraction_table': data_extraction_table,
            'finished_all_steps': finished_all_steps,
            'tab': tab,
            'unseen_comments': unseen_comments
        })

def bibtex_to_article_object(bib_database, review, source):
    articles = []
    if bib_database:
        for entry in bib_database.entries:
            article = Article()
            try:
                if 'id'              in entry: article.bibtex_key      = entry['id'][:100]
                if 'title'           in entry: article.title           = entry['title'][:1000]
                if 'journal'         in entry: article.journal         = entry['journal'][:1000]
                if 'year'            in entry: article.year            = entry['year'][:10]
                if 'author'          in entry: article.author          = entry['author'][:1000]
                if 'abstract'        in entry: article.abstract        = entry['abstract'][:4000]
                if 'pages'           in entry: article.pages           = entry['pages'][:20]
                if 'volume'          in entry: article.volume          = entry['volume'][:100]
                if 'type'            in entry: article.document_type   = entry['type'][:100]
                elif 'document_type' in entry: article.document_type   = entry['document_type'][:100]
                if 'doi'             in entry: article.doi             = entry['doi'][:50]
                if 'link'            in entry: article.url             = entry['link'][:500]
                elif 'url'           in entry: article.url             = entry['url'][:500]
                if 'affiliation'     in entry: article.affiliation     = entry['affiliation'][:500]
                if 'author_keywords' in entry: article.author_keywords = entry['author_keywords'][:500]
                if 'keywords'        in entry: article.keywords        = entry['keywords'][:500]
                elif 'keyword'       in entry: article.keywords        = entry['keyword'][:500]
                if 'publisher'       in entry: article.publisher       = entry['publisher'][:100]
                if 'issn'            in entry: article.issn            = entry['issn'][:50]
                if 'language'        in entry: article.language        = entry['language'][:50]
                if 'note'            in entry: article.note            = entry['note'][:500]
                article.review = review
                article.source = source
            except:
                continue
            articles.append(article)
    return articles

def _import_articles(request, source, articles):
    if any(articles):
        success = 0
        error = 0
        for article in articles:
            try:
                article.created_by = request.user
                article.save()
                success = success + 1
            except:
                error = error + 1
        if success > 0:
            messages.success(request, _('{0} articles successfully imported to {1}!').format(success, source.name))
        if error > 0:
            messages.warning(request, _('{0} articles could not be imported because of invalid format or invalid utf-8 string.').format(error))
    else:
        messages.warning(request, _('The bibtex file had no valid entry!'))

@author_required
@login_required
@require_POST
def import_bibtex(request):
    review_id = request.POST['review-id']
    source_id = request.POST['source-id']

    review = Review.objects.get(pk=review_id)
    source = Source.objects.get(pk=source_id)

    bibtex_file = request.FILES['bibtex']

    ext = os.path.splitext(bibtex_file.name)[1]
    valid_extensions = ['.bib', '.bibtex']

    if ext in valid_extensions or bibtex_file.content_type == 'application/x-bibtex':
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        bib_database = bibtexparser.load(bibtex_file, parser=parser)
        articles = bibtex_to_article_object(bib_database, review, source)
        _import_articles(request, source, articles)
    else:
        messages.error(request, _('Invalid file type. Only .bib or .bibtex files are accepted.'))

    return redirect(r('import_studies', args=(review.author.username, review.name)))

@author_required
@login_required
@require_POST
def import_bibtex_raw_content(request):
    review_id = request.POST.get('review-id')
    source_id = request.POST.get('source-id')
    bibtex_file = request.POST.get('bibtex_file')

    review = Review.objects.get(pk=review_id)
    source = Source.objects.get(pk=source_id)

    parser = BibTexParser()
    parser.customization = convert_to_unicode
    bib_database = bibtexparser.loads(bibtex_file, parser=parser)
    articles = bibtex_to_article_object(bib_database, review, source)
    _import_articles(request, source, articles)

    return redirect(r('import_studies', args=(review.author.username, review.name)))

@author_or_visitor_required
@login_required
def source_articles(request):
    try:
        review_id = request.GET['review-id']
        source_id = request.GET['source-id']

        status_evaluation = ArticleEvaluation.ARTICLE_STATUS

        review = Review.objects.get(pk=review_id)
        if source_id != 'None':
            articles = review.get_source_articles(source_id)
            source = Source.objects.get(pk=source_id)
        else:
            articles = review.get_source_articles()
            source = Source()

        return render(request, 'conducting/partial_conducting_articles.html', {'review': review, 'source': source, 'articles': articles, 'status_evaluation': status_evaluation})
    except Exception as e:
        print e
        return HttpResponseBadRequest()

@author_or_visitor_required
@login_required
def article_details(request):
    try:
        review_id = request.GET['review-id']
        article_id = request.GET['article-id']
        user = request.user

        review = Review.objects.get(pk=review_id)
        article = Article.objects.get(pk=article_id)

        try:
            article_evaluation = ArticleEvaluation.objects.get(article__id=article_id, user__id=user.id)
        except ArticleEvaluation.DoesNotExist:
            article_evaluation = ArticleEvaluation(review=review, article=article, user=user)

        mendeley_files = []
        if user.profile.mendeley_token:
            mendeley_files = user.profile.get_mendeley_session().files.list().items
        context = RequestContext(request, { 'review': review, 'article': article, 'mendeley_files': mendeley_files, 'article_evaluation': article_evaluation })
        return render_to_response('conducting/partial_conducting_article_details.html', context)
    except Exception as e:
        print e
        return HttpResponseBadRequest()

@author_or_visitor_required
@login_required
def article_details_confirm(request):
    try:
        review_id = request.GET['review-id']
        article_id = request.GET['article-id']
        user = request.user

        review = Review.objects.get(pk=review_id)
        article = Article.objects.get(pk=article_id)

        context = RequestContext(request, { 'review': review, 'article': article })
        return render_to_response('conducting/partial_conducting_article_details_confirm.html', context)
    except Exception as e:
        print e
        return HttpResponseBadRequest()

@author_required
@login_required
def articles_upload(request):
    try:
        if request.method == 'POST':
            form = ArticleUploadForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded_file = request.FILES['article_file']

                review_id = request.POST.get('review-id')
                review = Review.objects.get(pk=review_id)

                article_id = request.POST.get('article-id')
                article = Article.objects.get(pk=article_id)
                hasFile = ArticleFile.objects.filter(review=review, article=article).count()
                if not hasFile:
                    article_file = ArticleFile(review=review,
                            article=article,
                            user=request.user,
                            article_file=uploaded_file,
                            name=uploaded_file.name,
                            size=uploaded_file.size)
                    article_file.save()

                    #context = RequestContext(request, {'file': article_file })
                    #return render_to_response('conducting/partial_article_files_row.html', context)
                    return reload_article_files_tab(request, article_id)
                else:
                    return HttpResponseBadRequest(_('File has already updated. Only one file per article is permitted. Delete existing file to upload new.'))

            else:
                error = form['article_file'].errors.as_data()[0]
                return HttpResponseBadRequest(error)
    except Exception as e:
        print e
        return HttpResponseBadRequest()

@author_required
@login_required
def remove_article_file(request):
    try:
        file_id = request.POST['file-id']
        if file_id != 'None':
            try:
                file = ArticleFile.objects.get(pk=file_id)
                article_id = file.article.id
                file.delete()
                return reload_article_files_tab(request, article_id)
            except ArticleFile.DoesNotExist:
                return HttpResponseBadRequest()

        return HttpResponse()
    except Exception as e:
        print e
        return HttpResponseBadRequest()

def reload_article_files_tab(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
        context = RequestContext(request, {"article": article})
        return render_to_response('conducting/partial_article_files.html', context)
    except Exception as e:
        return HttpResponseBadRequest()

def build_article_table_row(request, article, user):
    status_evaluation = ArticleEvaluation.ARTICLE_STATUS
    name = ''
    if article.created_by:
        name = escape(article.created_by.profile.get_screen_name())
    date = ''
    if article.created_at:
        date = article.created_at.strftime('%d %b %Y %H:%M:%S')

    context = RequestContext(request, {'article': article, 'user': user, 'status_evaluation': status_evaluation})
    return render_to_response('conducting/partial_conducting_article_row.html', context)


@author_required
@login_required
def save_article_details(request):
    if request.method == 'POST':
        try:
            article_id = request.POST['article-id']

            if article_id != 'None':
                article = Article.objects.get(pk=article_id)
            else:
                review_id = request.POST['review-id']
                source_id = request.POST['source-id']
                review = Review.objects.get(pk=review_id)
                source = Source.objects.get(pk=source_id)
                article = Article(review=review, source=source)

            article.bibtex_key = request.POST['bibtex-key'][:100]
            article.title = request.POST['title'][:1000]
            article.author = request.POST['author'][:1000]
            article.journal = request.POST['journal'][:1000]
            article.year = request.POST['year'][:10]
            article.pages = request.POST['pages'][:20]
            article.volume = request.POST['volume'][:100]
            article.author = request.POST['author'][:1000]
            article.abstract = request.POST['abstract'][:4000]
            article.document_type = request.POST['document-type'][:100]
            article.doi = request.POST['doi'][:50]
            article.url = request.POST['url'][:500]
            article.affiliation = request.POST['affiliation'][:500]
            article.author_keywords = request.POST['author_keywords'][:500]
            article.keywords = request.POST['keywords'][:500]
            article.publisher = request.POST['publisher'][:100]
            article.issn = request.POST['issn'][:50]
            article.language = request.POST['language'][:50]
            article.note = request.POST['note'][:500]
            article.updated_by = request.user
            article.save()

            return HttpResponse(build_article_table_row(request, article, request.user))
        except Exception as e:
            print e
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

@author_required
@login_required
def save_article_details_confirm(request):
    if request.method == 'POST':
        try:
            article_id = request.POST['article-id']

            if article_id != 'None':
                article = Article.objects.get(pk=article_id)
            else:
                review_id = request.POST['review-id']
                source_id = request.POST['source-id']
                review = Review.objects.get(pk=review_id)
                source = Source.objects.get(pk=source_id)
                article = Article(review=review, source=source)

            article.bibtex_key = request.POST['bibtex-key'][:100]
            article.title = request.POST['title'][:1000]
            article.author = request.POST['author'][:1000]
            article.journal = request.POST['journal'][:1000]
            article.year = request.POST['year'][:10]
            article.abstract = request.POST['abstract'][:4000]

            article.updated_by = request.user
            article.save()

            return HttpResponse(build_article_table_row(request, article, request.user))
        except Exception as e:
            print e
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

@author_required
@login_required
def save_article_evaluation(request):
    if request.method == 'POST':
        try:
            article_id = request.POST['article-id']
            article_evaluation_id = request.POST['article-evaluation-id']
            review_id = ''

            if article_evaluation_id != 'None':
                article_evaluation = ArticleEvaluation.objects.get(pk=article_evaluation_id)
                review_id = article_evaluation.review.id
            else:
                review_id = request.POST['review-id']
                review = Review.objects.get(pk=review_id)
                article = Article.objects.get(pk=article_id)
                article_evaluation = ArticleEvaluation(review=review, article=article, user=request.user)

            article_evaluation.comments = ''
            status = request.POST['status'][:1]
            if status in (ArticleEvaluation.UNCLASSIFIED, ArticleEvaluation.REJECTED, ArticleEvaluation.ACCEPTED, ArticleEvaluation.DUPLICATED):
                article_evaluation.status = status

            selection_criteria_id = request.POST.get('selection_criteria')
            try:
                selection_criteria = SelectionCriteria.objects.get(pk=selection_criteria_id)
                article_evaluation.selection_criteria = selection_criteria
            except:
                article_evaluation.selection_criteria = None

            article_evaluation.save()

            edit_article_status(review_id, article_id)

            return HttpResponse()
        except Exception as e:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

def edit_article_status(review_id, article_id):
    try:
        review = Review.objects.get(pk=review_id)
        article_evaluations = ArticleEvaluation.objects.filter(review__id=review_id, article__id=article_id)
        article = Article.objects.get(pk=article_id)
        previous_status = ''


        if not article.evaluation_finished:
            if article_evaluations.count() == 0:
                article.status = 'U'
            elif article_evaluations.count() == 1 and review.co_authors.count() == 0:
                article.status = article_evaluations[0].status
            elif article_evaluations.count() == 1:
                article.status = 'W'
            else:
                for evaluation in article_evaluations:
                    if previous_status == '':
                        previous_status = evaluation.status
                    else:
                        if evaluation.status != previous_status:
                            article.status = 'C'
                            article.save()
                            return HttpResponse()
                        else:
                            previous_status = evaluation.status
                            article.status = evaluation.status

            article.save()

        return HttpResponse()
    except Exception as e:
        print e
        return HttpResponseBadRequest()

@author_required
@login_required
def article_solve_conflict(request):
    try:
        review_id = request.POST['review-id']
        article_id = request.POST['article-id']
        article = Article.objects.get(pk=article_id)

        status = request.POST['status'][:1]
        if status in (Article.UNCLASSIFIED, Article.WAITING, Article.REJECTED, Article.CONFLICT, Article.ACCEPTED, Article.DUPLICATED):
            article.status = status
            article.evaluation_finished = True

            article.save()

        return HttpResponse()
    except:
        return HttpResponseBadRequest()

@author_required
@login_required
def save_quality_assessment(request):
    try:
        article_id = request.POST['article-id']
        question_id = request.POST['question-id']
        answer_id = request.POST['answer-id']

        article = Article.objects.get(pk=article_id)
        question = QualityQuestion.objects.get(pk=question_id)
        answer = QualityAnswer.objects.get(pk=answer_id)

        quality_assessment, created = QualityAssessment.objects.get_or_create(article=article, question=question)
        quality_assessment.answer = answer
        quality_assessment.save()

        return HttpResponse(article.get_score())
    except:
        return HttpResponseBadRequest()


@author_or_visitor_required
@login_required
def quality_assessment_detailed(request):
    try:
        review_id = request.GET['review-id']
        review = Review.objects.get(pk=review_id)
        order = request.session.get('quality_assessment_order', 'title')
        quality_assessment_table = build_quality_assessment_table(request, review, order)
        context = RequestContext(request, {'review': review, 'quality_assessment_table': quality_assessment_table, 'order': order})
        return render_to_response('conducting/partial_conducting_quality_assessment_detailed.html', context)
    except:
        return HttpResponseBadRequest()


@author_or_visitor_required
@login_required
def quality_assessment_summary(request):
    try:
        review_id = request.GET['review-id']
        review = Review.objects.get(pk=review_id)
        context = RequestContext(request, {'review': review, })
        return render_to_response('conducting/partial_conducting_quality_assessment_summary.html', context)
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def multiple_articles_action_remove(request):
    try:
        article_ids = request.POST['article_ids']
        article_ids_list = article_ids.split('|')
        if article_ids_list:
            Article.objects.filter(pk__in=article_ids_list).delete()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def multiple_articles_action_accept(request):
    try:
        article_ids = request.POST['article_ids']
        article_ids_list = article_ids.split('|')
        if article_ids_list:
            Article.objects.filter(pk__in=article_ids_list).update(status=Article.ACCEPTED)
        return HttpResponse()
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def multiple_articles_action_reject(request):
    try:
        article_ids = request.POST['article_ids']
        article_ids_list = article_ids.split('|')
        if article_ids_list:
            Article.objects.filter(pk__in=article_ids_list).update(status=Article.REJECTED)
        return HttpResponse()
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def multiple_articles_action_duplicated(request):
    try:
        article_ids = request.POST['article_ids']
        article_ids_list = article_ids.split('|')
        if article_ids_list:
            Article.objects.filter(pk__in=article_ids_list).update(status=Article.DUPLICATED)
        return HttpResponse()
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def save_empirical_value_field(request):
    try:
        review_id = request.GET['review-id']
        article_id = request.GET['article-id']
        n1 = request.GET['n1']
        dp1 = request.GET['dp1']
        a1 = request.GET['a1']
        n2 = request.GET['n2']
        dp2 = request.GET['dp2']
        a2 = request.GET['a2']
        data_type = request.GET['data-type']
        effect_size = request.GET['effect-size']
        min_limit = request.GET['min-limit']
        max_limit = request.GET['max-limit']
        std_error = request.GET['std-error']

        if len(dp1) > 12 or len(a1) > 12 or len(dp2) > 12 or len(a2) > 12:
            return HttpResponseBadRequest(_('Empirical value fields do not accept values greater than 12 digits for dp and a.'))

        if len(effect_size) > 12 or len(min_limit) > 12 or len(max_limit) > 12 or len(std_error) > 12:
            return HttpResponseBadRequest(_('Empirical value fields do not accept values greater than 12 digits for effect size, max limit, min limit and standard error.'))

        article = Article.objects.get(pk=article_id)
        empirical_values, created = ArticleEmpiricalData.objects.get_or_create(article=article)
        if n1:
            empirical_values.n1 = n1
        if dp1:
            empirical_values.dp1 = dp1
        if a1:
            empirical_values.a1 = a1
        if n2:
            empirical_values.n2 = n2
        if dp2:
            empirical_values.dp2 = dp2
        if a2:
            empirical_values.a2 = a2
        if data_type:
            empirical_values.data_type = data_type
        if effect_size:
            empirical_values.effect_size = effect_size
        if min_limit:
            empirical_values.min_limit = min_limit
        if max_limit:
            empirical_values.max_limit = max_limit
        if std_error:
            empirical_values.std_error = std_error

        empirical_values.save()

        return HttpResponse()

    except Exception, e:
        return HttpResponseBadRequest(e)

@author_required
@login_required
def save_data_extraction(request):
    try:
        article_id = request.POST['article-id']
        field_id = request.POST['field-id']
        value = request.POST['value']

        article = Article.objects.get(pk=article_id)
        field = DataExtractionField.objects.get(pk=field_id)
        if article.review.is_author_or_coauthor(request.user):
            data_extraction, created = DataExtraction.objects.get_or_create(article=article, field=field)
            data_extraction.set_value(value)
            data_extraction.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
    except Exception, e:
        return HttpResponseBadRequest(e)

@author_required
@login_required
def save_data_extraction_status(request):
    print 'save_data_extraction_status'
    try:
        article_id = request.POST.get('article-id')
        action = request.POST.get('action')
        is_finished = (action == 'mark_as_done')

        article = Article.objects.get(pk=article_id)
        article.finished_data_extraction = is_finished
        article.save()
        return HttpResponse()
    except Exception, e:
        return HttpResponseBadRequest(e)

@author_required
@login_required
def find_duplicates(request):
    review_id = request.GET['review-id']
    review = Review.objects.get(pk=review_id)
    duplicates = review.get_duplicate_articles()
    context = RequestContext(request, {'duplicates': duplicates})
    return render_to_response('conducting/partial_conducting_find_duplicates.html', context)


@author_required
@login_required
def resolve_duplicated(request):
    try:
        article_id = request.POST['article-id']
        article = Article.objects.get(pk=article_id)
        if article.review.is_author_or_coauthor(request.user):
            article.status = Article.DUPLICATED
            article.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
    except Exception, e:
        return HttpResponseBadRequest()


@author_required
@login_required
def resolve_all(request):
    try:
        article_id_list = []
        review_id = request.POST['review-id']
        review = Review.objects.get(pk=review_id)
        duplicates = review.get_duplicate_articles()
        for duplicate in duplicates:
            for i in range(1, len(duplicate)):
                duplicate[i].status = Article.DUPLICATED
                duplicate[i].save()
                article_id_list.append(str(duplicate[i].id))
        return HttpResponse(','.join(article_id_list))
    except Exception, e:
        return HttpResponseBadRequest()


@author_required
@login_required
def new_article(request):
    review_id = request.GET['review-id']
    source_id = request.GET['source-id']

    review = Review.objects.get(pk=review_id)
    source = Source.objects.get(pk=source_id)

    article = Article(review=review, source=source)

    context = RequestContext(request, {'article': article})
    return render_to_response('conducting/partial_conducting_article_details.html', context)

@author_or_visitor_required
@login_required
def data_analysis(request, username, review_name):
    review = get_object_or_404(Review, name=review_name, author__username__iexact=username)
    unseen_comments = review.get_visitors_unseen_comments(request.user)
    analysis = ''
    if review.is_metaanalysis:
        analysis = article_meta_analysis(review, request)
    return render(request, 'conducting/conducting_data_analysis.html', { 'review': review, 'unseen_comments': unseen_comments, 'analysis': analysis })

def article_conclusion_effect(review, article, effect_size):
    setup = review.get_search_setup()[0]
    conclusion = {}

    conclusion['article_id'] = article.id
    conclusion['article'] = article.title
    conclusion['effect_size'] = effect_size

    if effect_size < 0:
        conclusion['effect'] = setup.adverse_effect
    if effect_size >= 0.0 and effect_size <= 0.1:
        if setup.conclusion_model == 'COHEN':
            conclusion['effect'] = setup.no_effect
        elif setup.conclusion_model == 'HATTIE':
            conclusion['effect'] = setup.developmental_effects
    if effect_size >= 0.2 and effect_size <= 0.4 and setup.conclusion_model == 'COHEN':
        conclusion['effect'] = setup.small_effect
    if effect_size >= 0.2 and effect_size <= 0.3 and setup.conclusion_model == 'HATTIE':
        conclusion['effect'] = setup.teacher_effects
    if effect_size >= 0.5 and effect_size <= 0.7 and setup.conclusion_model == 'COHEN':
        conclusion['effect'] = setup.intermediate_effect
    if effect_size >= 0.4 and setup.conclusion_model == 'HATTIE':
        conclusion['effect'] = setup.zone_desired_effects
    if effect_size >= 0.8 and setup.conclusion_model == 'COHEN':
        conclusion['effect'] = setup.large_effect

    return conclusion

def article_meta_analysis(review, request):
    try:
        articles = review.get_final_selection_articles()
        analysis = {}
        dataset = []
        conclusions = []
        payload = {
            "studies": [],
            "efs": {},
            "labels": {
                "study_label": _("Study"),
                "efs_label": _("Effect Size"),
                "summary_label": _("Summarization")
            }
        }

        for article in articles:
            if article.has_empirical_data and article.finished_data_extraction:
                values = article.get_empirical_values()
                if values.count() > 0:
                    data = values[0]
                    if data.data_type == 'P':
                        if data.n1 and data.n2 and data.dp1 and data.dp2 and data.a1 and data.a2:
                            result = cohen_d(data.n1, data.dp1, data.n2, data.dp2, data.a1, data.a2)
                            dataset.append([str(article.title), result['cohen_d'], result['ci_min'], result['ci_max'], result['std_error']])
                            conclusions.append(article_conclusion_effect(review, article, result['cohen_d']))
                            payload['studies'].append({
                                "name": str(article.title),
                                "mean": str(result['cohen_d']),
                                "lower": str(result['ci_min']),
                                "upper": str(result["ci_max"])
                            })

                        else:
                            messages.error(request, _('Your article {0} do not have all empirical values. Because of this, the Sumarize Tool can not generate meta analysis forest plot graphic.').format(article.title))

                    elif data.data_type == 'E':
                        if data.effect_size and data.min_limit and data.max_limit and data.std_error:
                            dataset.append([str(article.title), float(data.effect_size), float(data.min_limit), float(data.max_limit), float(data.std_error)])
                            conclusions.append(article_conclusion_effect(review, article, data.effect_size))
                            payload['studies'].append({
                                "name": str(article.title),
                                "mean": str(data.effect_size),
                                "lower": str(data.min_limit),
                                "upper": str(data.max_limit)
                            })

                        else:
                            messages.error(request, _('Your article {0} do not have all empirical values. Because of this, the Sumarize Tool can not generate meta analysis forest plot graphic.').format(article.title))

        payload['efs']['mean'] = str(effect_size_comb(dataset))
        payload['efs']['lower'] = str(cin_efs_lower_limit(dataset))
        payload['efs']['upper'] = str(cin_efs_max_limit(dataset))

        print 'payload ', payload

        headers = {'Content-Type': 'application/json'}
        forest = requests.post(config('FOREST_PLOT_URL'), data=json.dumps(payload), headers=headers)

        analysis['dataset'] = dataset
        analysis['forest_plot'] = forest._content
        analysis['conclusions'] = conclusions
        return analysis

    except ZeroDivisionError:
        messages.error(request,_('The empirical values from any of your articles are not valid! Because of this, the Sumarize Tool can not generate meta analysis forest plot graphic.'))


def articles_selection_chart(request):
    review_id = request.GET['review-id']
    review = Review.objects.get(pk=review_id)
    selected_articles = review.get_accepted_articles()
    articles = []
    for source in review.sources.all():
        count = review.get_source_articles(source.id).count()
        accepted_count = selected_articles.filter(source__id=source.id).count()
        articles.append(source.name + ':' + str(count) + ':' + str(accepted_count))
    return HttpResponse(','.join(articles))

def articles_per_year(request):
    review_id = request.GET['review-id']
    review = Review.objects.get(pk=review_id)
    final_articles = review.get_final_selection_articles().values('year').annotate(count=Count('year')).order_by('-year')
    articles = []
    for article in final_articles:
        articles.append(article['year'] + ':' + str(article['count']))
    return HttpResponse(','.join(articles))

@author_required
@login_required
@require_POST
def add_source_string(request):
    review_id = request.POST.get('review-id')
    review = get_object_or_404(Review, pk=review_id)
    source_ids = request.POST.getlist('source')
    for source_id in source_ids:
        try:
            source = Source.objects.get(pk=source_id)
            exists = SearchSession.objects.filter(review=review, source=source).exists()
            if not exists:
                search_session = SearchSession(review=review, source=source)
                search_session.save()
        except Source.DoesNotExist:
            pass
    review.save()
    messages.success(request, _('Sources search string successfully added to the review!'))
    return redirect(r('search_studies', args=(review.author.username, review.name)))


@author_required
@login_required
@require_POST
def export_results(request):
    review_id = request.POST.get('review-id')
    review = get_object_or_404(Review, pk=review_id)
    articles = review.get_source_articles()

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=articles.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Articles")

    row_num = 0

    columns = [
        ('bibtex_key', 2000),
        ('title', 2000),
        ('author', 2000),
        ('journal', 2000),
        ('year', 2000),
        ('source', 2000),
        ('pages', 2000),
        ('volume', 2000),
        ('abstract', 2000),
        ('document_type', 2000),
        ('doi', 2000),
        ('url', 2000),
        ('affiliation', 2000),
        ('author_keywords', 2000),
        ('keywords', 2000),
        ('publisher', 2000),
        ('issn', 2000),
        ('language', 2000),
        ('note', 2000),
        ('selection_criteria', 2000),
        ('created_at', 2000),
        ('updated_at', 2000),
        ('created_by', 2000),
        ('updated_by', 2000),
        ('status', 2000),
        ('comments', 2000),
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    row_num += 1

    for article in articles:
        try:
            row = [
                article.bibtex_key,
                article.title,
                article.author,
                article.journal,
                article.year,
                (article.source.name if article.source else ''),
                article.pages,
                article.volume,
                article.abstract,
                article.document_type,
                article.doi,
                article.url,
                article.affiliation,
                article.author_keywords,
                article.keywords,
                article.publisher,
                article.issn,
                article.language,
                article.note,
                (article.selection_criteria.description if article.selection_criteria else '' ),
                article.created_at.replace(tzinfo=None),
                article.updated_at.replace(tzinfo=None),
                (article.created_by.username if article.created_by else ''),
                (article.updated_by.username if article.updated_by else ''),
                article.get_status_display(),
                article.comments,
            ]
            for col_num in xrange(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
        except Exception, e:
            ws.write(row_num, 0, u'Error: {0}'.format(e.message), font_style)

        row_num += 1

    wb.save(response)
    return response


@author_required
@login_required
@require_POST
def export_data_extraction(request):
    review_id = request.POST.get('review-id')
    review = get_object_or_404(Review, pk=review_id)

    selected_studies = review.get_final_selection_articles()
    data_extraction_fields = review.get_data_extraction_fields()

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=data_extraction.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Articles")

    row_num = 0

    columns = [
        ('article', 2000),
    ]
    for field in data_extraction_fields:
        columns.append((field.description, 2000))

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    row_num += 1

    for article in selected_studies:
        try:
            row = [article.title,]
            for field in data_extraction_fields:
                field_value = None
                try:
                    de = DataExtraction.objects.get(article=article, field=field)
                    if de.field.field_type == DataExtractionField.DATE_FIELD:
                        field_value = de.get_date_value_as_string()
                    elif de.field.field_type == DataExtractionField.SELECT_ONE_FIELD:
                        select_one_field = de._get_select_one_value()
                        if select_one_field:
                            field_value = select_one_field.value
                        else:
                            field_value = ''
                    elif de.field.field_type == DataExtractionField.SELECT_MANY_FIELD:
                        field_value = ', '.join(de._get_select_many_value().values_list('value', flat=True))
                    else:
                        field_value = de.value
                except DataExtraction.DoesNotExist:
                    field_value = ''
                row.append(field_value)

            for col_num in xrange(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
        except Exception, e:
            ws.write(row_num, 0, u'Error: {0}'.format(e.message), font_style)

        row_num += 1

    wb.save(response)
    return response
@login_required
def new_document(request):
    json_context = {}
    source_id = 0
    review_id = 0
    if request.method == 'POST':
        source_id = request.POST.get('source_id')
        review_id = request.POST.get('review_id')


        form = DocumentForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            document = form.save()

            source = Source.objects.get(pk=source_id)
            review = Review.objects.get(pk=review_id)


            article = Article(review=review, source=source)

            article.build(document)
            article.created_by = request.user
            article.save()

            messages.success(request, _('Document added successfully!'))
            json_context['status'] = 'success'
            json_context['redirect_to'] =  request.get_full_path()
        else:
            json_context['status'] = 'error'
    else:
        source_id = request.GET.get('source-id')
        review_id = request.GET.get('review-id')

        form = DocumentForm()
        json_context['status'] = 'ok'
    csrf_token = unicode(csrf(request)['csrf_token'])
    html = render_to_string('conducting/new_document.html', { 'form': form, 'csrf_token': csrf_token, 'review_id': review_id, 'source_id': source_id})
    json_context['html'] = html
    dump = json.dumps(json_context)
    return HttpResponse(dump, content_type='application/json')
