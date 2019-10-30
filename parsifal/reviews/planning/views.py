# -*- coding: utf-8 -*-

import time
import json

from django.db import transaction
from django.db.models import Q
from django.core.urlresolvers import reverse as r
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.utils.html import escape


from parsifal.reviews.models import *
from parsifal.reviews.planning.forms import KeywordForm, SynonymForm
from parsifal.reviews.decorators import main_author_required, author_required, author_or_visitor_required


from django.utils.translation import ugettext as _


@author_or_visitor_required
@login_required
def planning(request, username, review_name):
    return redirect(r('protocol', args=(username, review_name)))

@author_or_visitor_required
@login_required
def protocol(request, username, review_name):
    review = get_object_or_404(Review, name=review_name, author__username__iexact=username)
    unseen_comments = review.get_visitors_unseen_comments(request.user)
    return render(request, 'planning/protocol.html', { 'review': review, 'unseen_comments': unseen_comments })

@author_or_visitor_required
@login_required
def quality_assessment_checklist(request, username, review_name):
    review = get_object_or_404(Review, name=review_name, author__username__iexact=username)
    unseen_comments = review.get_visitors_unseen_comments(request.user)
    return render(request, 'planning/quality_assessment_checklist.html', { 'review': review, 'unseen_comments': unseen_comments })

@author_or_visitor_required
@login_required
def risks_to_review_validity(request, username, review_name):
    review = get_object_or_404(Review, name=review_name, author__username__iexact=username)
    unseen_comments = review.get_visitors_unseen_comments(request.user)
    return render(request, 'planning/risks_to_review_validity.html', { 'review': review, 'unseen_comments': unseen_comments })

@author_or_visitor_required
@login_required
def data_extraction_form(request, username, review_name):
    review = get_object_or_404(Review, name=review_name, author__username__iexact=username)
    unseen_comments = review.get_visitors_unseen_comments(request.user)
    empty_field = DataExtractionField()
    return render(request, 'planning/data_extraction_form.html', { 'review': review, 'unseen_comments': unseen_comments, 'empty_field': empty_field })

def statistical_methods_conventions(request, username, review_name):
    review = get_object_or_404(Review, name=review_name, author__username__iexact=username)
    unseen_comments = review.get_visitors_unseen_comments(request.user)
    return render(request, 'planning/statistical_methods_conventions.html', { 'review': review, 'unseen_comments': unseen_comments })

def save_statistical_methods(request):
    try:
        review_id = request.POST['review-id']
        statistical_methods = request.POST['statistical_methods']
        review = Review.objects.get(pk=review_id)
        if len(statistical_methods) > 1000:
            return HttpResponseBadRequest(_('The review statistical and methods should not exceed 1000 characters. The given statistical and methods have %s characters.') % len(statistical_methods))
        else:
            review.statistical_methods = statistical_methods
            review.save()
            return HttpResponse(_('Your review have been saved successfully!'))
    except:
        return HttpResponseBadRequest()


@author_or_visitor_required
@login_required
def search_setup(request, username, review_name):
    review = get_object_or_404(Review, name=review_name, author__username__iexact=username)
    unseen_comments = review.get_visitors_unseen_comments(request.user)

    try:
        setup = SearchSetup.objects.get(review=review)
    except:
        setup = SearchSetup(review=review)
        setup.save()

    return render(request, 'planning/search_setup.html', { 'review': review, 'unseen_comments': unseen_comments, 'setup': setup })

@author_required
@login_required
def save_search_setup(request):
    try:
        review_id = request.POST['review-id']
        is_metaanalysis = request.POST['is_metaanalysis']
        is_metaanalysis = True if is_metaanalysis == 'True' else False

        review = Review.objects.get(pk=review_id)
        setup = SearchSetup.objects.get(review=review)
        if is_metaanalysis:

            conclusion_model = request.POST['conclusion_model']
            adverse_effect = request.POST['adverse_effect']
            no_effect = request.POST['no_effect']
            small_effect = request.POST['small_effect']
            intermediate_effect = request.POST['intermediate_effect']
            large_effect = request.POST['large_effect']
            developmental_effects = request.POST['developmental_effects']
            teacher_effects = request.POST['teacher_effects']
            zone_desired_effects = request.POST['zone_desired_effects']

            setup.conclusion_model = conclusion_model
            setup.adverse_effect = adverse_effect
            setup.no_effect = no_effect
            setup.small_effect = small_effect
            setup.intermediate_effect = intermediate_effect
            setup.large_effect = large_effect
            setup.developmental_effects = developmental_effects
            setup.teacher_effects = teacher_effects
            setup.zone_desired_effects = zone_desired_effects

            setup.save()
        else:
            if setup:
                setup.delete()

        review.is_metaanalysis = is_metaanalysis

        review.save()

        return HttpResponse(_('Your review search setup have been saved successfully!'))
    except Exception as e:
        print 'erro ', e
        return HttpResponseBadRequest()


'''
    OBJECTIVE FUNCTIONS
'''

@author_required
@login_required
def save_objective(request):
    try:
        review_id = request.POST['review-id']
        objective = request.POST['objective']
        review = Review.objects.get(pk=review_id)
        if len(objective) > 1000:
            return HttpResponseBadRequest(_('The review objectives should not exceed 1000 characters. The given objectives have %s characters.') % len(objective))
        else:
            review.objective = objective
            review.save()
            return HttpResponse(_('Your review have been saved successfully!'))
    except:
        return HttpResponseBadRequest()


'''
    QUESTION FUNCTIONS
'''

@author_required
@login_required
def save_question(request):
    '''
        Function used via Ajax request only.
        This function takes a review question form and save on the database
    '''
    try:
        review_id = request.POST['review-id']
        question_id = request.POST['question-id']
        description = request.POST['description']
        review = Review.objects.get(pk=review_id)
        try:
            question = Question.objects.get(pk=question_id)
        except:
            question = Question(review=review)
        question.question = description[:500]
        question.save()
        context = RequestContext(request, {'question':question})
        return render_to_response('planning/partial_planning_question.html', context)
    except:
        return HttpResponseBadRequest()

@author_required
@login_required
def save_question_order(request):
    try:
        orders = request.POST.get('orders')
        question_orders = orders.split(',')
        for question_order in question_orders:
            if question_order:
                question_id, order = question_order.split(':')
                question = Question.objects.get(pk=question_id)
                question.order = order
                question.save()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()

@author_required
@login_required
def add_or_edit_question(request):
    '''
        Function used via Ajax request only.
        This functions adds a new secondary question to the review.
    '''
    try:
        review_id = request.POST['review-id']
        question_id = request.POST['question-id']
        review = Review.objects.get(pk=review_id)
        try:
            question = Question.objects.get(pk=question_id)
        except:
            question = Question(review=review)
        context = RequestContext(request, {'question':question})
        return render_to_response('planning/partial_planning_question_form.html', context)
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def remove_question(request):
    '''
        Function used via Ajax request only.
        This function removes a secondary question from the review.
    '''
    try:
        review_id = request.POST['review-id']
        question_id = request.POST['question-id']
        if question_id != 'None':
            try:
                question = Question.objects.get(pk=question_id)
                question.delete()
            except Question.DoesNotExist:
                return HttpResponseBadRequest()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()


'''
    PICOC FUNCTIONS
'''

@author_required
@login_required
def save_picoc(request):
    try:

        review_id = request.POST['review-id']
        review = Review.objects.get(pk=review_id)
        if review.pico_type in ['PICOC','PICOS']:
            review.population = request.POST['population'][:200]
            review.intervention = request.POST['intervention'][:200]
            review.comparison = request.POST['comparison'][:200]
            review.outcome = request.POST['outcome'][:200]

        if review.pico_type == 'PICOC':
            review.context = request.POST['context'][:200]
        if review.pico_type == 'PICOS':
            review.study_type = request.POST['study_type'][:200]
        if review.pico_type == 'Free Text':
            review.pico_text = request.POST['pico_text'][:1000]
        review.save()
        return HttpResponse()
    except Exception, e:
        return HttpResponseBadRequest()


'''
    KEYWORDS/SYNONYM FUNCTIONS
'''

def extract_keywords(review, pico):
    if pico == Keyword.POPULATION: keywords = review.population
    elif pico == Keyword.INTERVENTION: keywords = review.intervention
    elif pico == Keyword.COMPARISON: keywords = review.comparison
    elif pico == Keyword.OUTCOME: keywords = review.outcome
    keyword_list = keywords.split(',')
    keyword_objects = []
    for term in keyword_list:
        if len(term) > 0:
            keyword = Keyword(review=review, description=term.strip(), related_to=pico)
            if keyword.description not in review.get_keywords().values_list('description', flat=True):
                keyword.save()
                keyword_objects.append(keyword)
    return keyword_objects


@author_required
@login_required
def import_pico_keywords(request):
    try:
        review_id = request.GET['review-id']
        review = Review.objects.get(pk=review_id)
        keywords = []

        keywords += extract_keywords(review, Keyword.POPULATION)
        keywords += extract_keywords(review, Keyword.INTERVENTION)
        keywords += extract_keywords(review, Keyword.COMPARISON)
        keywords += extract_keywords(review, Keyword.OUTCOME)
        #keywords += extract_keywords(review, Keyword.STUDY_TYPE)

        html = u''

        for keyword in keywords:
            context = RequestContext(request, { 'keyword': keyword })
            html += render_to_string('planning/partial_keyword.html', context)
        return HttpResponse(html)
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def remove_keyword(request):
    try:
        review_id = request.GET['review-id']
        keyword_id = request.GET['keyword-id']
        review = Review.objects.get(pk=review_id)
        keyword = Keyword.objects.get(pk=keyword_id)
        synonyms = Keyword.objects.filter(synonym_of__id=keyword_id)
        for synonym in synonyms:
            synonym.delete()
        keyword.delete()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()

@transaction.atomic
@author_required
@login_required
def add_keyword(request):
    review_id = request.GET.get('review-id', request.POST.get('review-id'))
    review = Review.objects.get(pk=review_id)
    SynonymFormSet = formset_factory(SynonymForm)
    response = {}
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        formset = SynonymFormSet(request.POST, prefix='synonym')
        if form.is_valid() and formset.is_valid():
            form.instance.review = review
            keyword = form.save()
            for form in formset:
                if form.instance.description:
                    form.instance.review = review
                    form.instance.synonym_of = keyword
                    form.save()
            context = RequestContext(request, { 'keyword': keyword })
            response['status'] = 'ok'
            response['html'] = render_to_string('planning/partial_keyword.html', context)
            dump = json.dumps(response)
            return HttpResponse(dump, content_type='application/json')
        else:
            response['status'] = 'validation_error'
    else:
        form = KeywordForm()
        formset = SynonymFormSet(prefix='synonym')
        response['status'] = 'new'
    context = RequestContext(request, {
            'review': review,
            'form': form,
            'formset': formset
        })
    response['html'] = render_to_string('planning/partial_keyword_form.html', context)
    dump = json.dumps(response)
    return HttpResponse(dump, content_type='application/json')

@transaction.atomic
@author_required
@login_required
def edit_keyword(request):
    review_id = request.GET.get('review-id', request.POST.get('review-id'))
    keyword_id = request.GET.get('keyword-id', request.POST.get('keyword-id'))
    review = Review.objects.get(pk=review_id)
    keyword = Keyword.objects.get(pk=keyword_id)

    SynonymFormSet = inlineformset_factory(Keyword, Keyword, SynonymForm, extra=1)
    response = {}
    if request.method == 'POST':
        form = KeywordForm(request.POST, instance=keyword)
        formset = SynonymFormSet(request.POST, instance=keyword, prefix='synonym')
        if form.is_valid() and formset.is_valid():
            form.instance.review = review
            keyword = form.save()
            for form in formset:
                form.instance.review = review
                form.instance.synonym_of = keyword
            formset.save()
            context = RequestContext(request, { 'keyword': keyword })
            response['status'] = 'ok'
            response['html'] = render_to_string('planning/partial_keyword.html', context)
            dump = json.dumps(response)
            return HttpResponse(dump, content_type='application/json')
        else:
            response['status'] = 'validation_error'
    else:
        form = KeywordForm(instance=keyword)
        formset = SynonymFormSet(instance=keyword, prefix='synonym')
        response['status'] = 'new'
    context = RequestContext(request, {
            'review': review,
            'form': form,
            'formset': formset
        })
    response['html'] = render_to_string('planning/partial_keyword_form.html', context)
    dump = json.dumps(response)
    return HttpResponse(dump, content_type='application/json')

'''
    SEARCH STRING FUNCTIONS
'''

@author_required
@login_required
def generate_search_string(request):
    '''
        Function used via Ajax request only.
        Still have to refactor this function. This is just a first approach.
    '''
    review_id = request.GET['review-id']
    review = Review.objects.get(pk=review_id)

    keywords = []
    for key, value in Keyword.RELATED_TO:
        synonyms = []
        for keyword in review.keywords.filter(related_to=key, synonym_of=None):
            synonyms.append(u'"{0}"'.format(keyword.description))
            for synonym in keyword.synonyms.all():
                synonyms.append(u'"{0}"'.format(synonym.description))
        if any(synonyms):
            keywords.append(u'({0})'.format(u' OR '.join(synonyms)))

    return HttpResponse(' AND '.join(keywords))


@author_required
@login_required
def save_generic_search_string(request):
    try:
        review_id = request.POST['review-id']
        search_string = request.POST['search-string']
        review = Review.objects.get(pk=review_id)
        generic_search_string = review.get_generic_search_string()
        generic_search_string.search_string = search_string
        generic_search_string.save()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()


'''
    SOURCE FUNCTIONS
'''

def html_source(source):
    html = '<tr source-id="' + str(source.id) + '"><td>' + escape(source.name) + '</td>'
    if source.url:
        html += '<td><a href="' + escape(source.url) + '" target="_blank">' + escape(source.url) + '</a></td>'
    else:
        html += '<td>' + escape(source.url) + '</td>'
    if source.is_default:
        html += '<td class="text-right"><span data-toggle="tooltip" data-placement="top" data-container="body" title='+ _('It is not possible to edit Digital Librarys details') + '><button type="button" class="btn btn-sm btn-warning" disabled>' +_('edit') + '</button></span> <button type="button" class="btn btn-danger btn-sm js-start-remove">'+_('remove')+'</a></td></tr>'
    else:
        html += '<td class="text-right"><button type="button" class="btn btn-sm btn-warning btn-edit-source"><span class="glyphicon glyphicon-pencil"></span>'+ _('edit') +'</button> <button type="button" class="btn btn-danger btn-sm js-start-remove"><span class="glyphicon glyphicon-trash"></span> '+ _('remove')+'</a></td></tr>'
    return html


@author_required
@login_required
def save_source(request):
    '''
        Function used via Ajax request only.
        This function adds a new source to the source list of the review.
        To add the source successfully the logged in user must be the author or a co-author
        of the review.
        If the request receives a source_id, that means the source already exist so the function
        will just edit the existing source and save the model.
    '''
    try:
        review_id = request.GET['review-id']
        source_id = request.GET['source-id']
        name = request.GET['name'][:100]
        url = request.GET['url'][:200]

        review = Review.objects.get(pk=review_id)
        if source_id:
            try:
                source = Source.objects.get(pk=source_id)
                source.name = name
                source.set_url(url)
                source.save()
                review.sources.add(source)
                review.save()
            except Source.DoesNotExist:
                pass
        else:
            source = Source()
            source.name=name
            source.set_url(url)
            source.save()
            review.sources.add(source)
            review.save()
        return HttpResponse(html_source(source))
    except Exception, e:
        return HttpResponseBadRequest()


@author_required
@login_required
def remove_source_from_review(request):
    try:
        print 'pre-remove'
        source_id = request.GET['source-id']
        review_id = request.GET['review-id']
        source = Source.objects.get(pk=source_id)
        review = Review.objects.get(pk=review_id)
        review.sources.remove(source)
        
        print 'remove'
        if source.is_default:
            print 'remove source_articles'
            review.get_source_articles(source.id).delete()
            try:
                print 'remove searchsession_set'
                review.searchsession_set.filter(source=source).delete()
            except Exception, e:
                print str(e)
                pass
        else:
            print 'remove only source'
            source.delete()
        review.save()
        return HttpResponse()
    except Exception, e:
        print e
        return HttpResponseBadRequest(str(e))


@author_required
@login_required
def suggested_sources(request):
    try:
        review_id = request.GET['review-id']
        review = Review.objects.get(pk=review_id)
        review.sources
        default_sources = Source.objects.filter(is_default=True)
        sources = filter(lambda s: s not in review.sources.all(), default_sources)
        return_html = ''
        for source in sources:
            return_html += '''
            <tr>
              <td>
                <input type="checkbox" value="''' + str(source.id) + '''" name="source-id">
              </td>
              <td>''' + str(source.name) + '''</td>
              <td>
                <a href="''' + source.url + '''" target="_blank">''' + source.url + '''</a>
              </td>
            </tr>'''
        return HttpResponse(return_html)
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def add_suggested_sources(request):
    try:
        source_ids = request.POST.getlist('source-id')
        review_id = request.POST['review-id']
        review = Review.objects.get(pk=review_id)
        return_html = ''
        for source_id in source_ids:
            source = Source.objects.get(pk=source_id)
            review.sources.add(source)
            return_html += html_source(source)
        review.save()
        return HttpResponse(return_html)
    except:
        return HttpResponseBadRequest()


'''
    INCLUSION/EXCLUSION CRITERIA FUNCTIONS
'''

@author_required
@login_required
def add_criteria(request):
    try:
        review_id = request.GET['review-id']
        description = request.GET['criteria']
        criteria_type = request.GET['criteria-type']
        review = Review.objects.get(pk=review_id)
        criteria = SelectionCriteria(review=review, description=description, criteria_type=criteria_type)
        criteria.save()
        return HttpResponse('<option value="' + str(criteria.id) + '">' + escape(criteria.description) + '</option>')
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def remove_criteria(request):
    try:
        review_id = request.GET['review-id']
        review = Review.objects.get(pk=review_id)
        criteria_ids = request.GET['criteria-ids']
        ids = criteria_ids.split(',')
        for id in ids:
            criteria = SelectionCriteria.objects.get(pk=id)
            criteria.delete()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()

'''
    SELECTION REVIEWER FUNCTIONS
'''

@author_required
@login_required
def save_selection_reviewer(request):
    try:
        review_id = request.POST['review-id']
        selection_reviewer = request.POST['selection-reviewer']
        reviewer = User.objects.get(pk=selection_reviewer)
        review = Review.objects.get(pk=review_id)
        review.selection_reviewer = reviewer
        review.save()
        return HttpResponse(_('Your review have been saved successfully!'))
    except Exception as e:
        print e
        return HttpResponseBadRequest()

'''
    RISK FUNCTIONS
'''

@author_required
@login_required
def save_risk(request):
    '''
        Function used via Ajax request only.
        This function takes a review risk form and save on the database
    '''
    try:
        review_id = request.POST['review-id']
        risk_id = request.POST['risk-id']
        description = request.POST['description']
        review = Review.objects.get(pk=review_id)
        try:
            risk = Risk.objects.get(pk=risk_id)
        except:
            risk = Risk(review=review)
        risk.risk = description[:500]
        risk.save()

        context = RequestContext(request, {'risk':risk})
        return render_to_response('planning/partial_planning_risk.html', context)
    except:
        return HttpResponseBadRequest()

@author_required
@login_required
def save_risk_order(request):
    try:
        orders = request.POST.get('orders')
        risk_orders = orders.split(',')
        for risk_order in risk_orders:
            if risk_order:
                risk_id, order = risk_order.split(':')
                risk = Risk.objects.get(pk=risk_id)
                risk.order = order
                risk.save()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()

@author_required
@login_required
def add_or_edit_risk(request):
    '''
        Function used via Ajax request only.
        This functions adds a new secondary risk to the review.
    '''
    try:
        review_id = request.POST['review-id']
        risk_id = request.POST['risk-id']
        review = Review.objects.get(pk=review_id)
        try:
            risk = Risk.objects.get(pk=risk_id)
        except:
            risk = Risk(review=review)
        context = RequestContext(request, {'risk':risk})
        return render_to_response('planning/partial_planning_risk_form.html', context)
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def remove_risk(request):
    '''
        Function used via Ajax request only.
        This function removes a secondary risk from the review.
    '''
    try:
        review_id = request.POST['review-id']
        risk_id = request.POST['risk-id']
        if risk_id != 'None':
            try:
                risk = Risk.objects.get(pk=risk_id)
                risk.delete()
            except Risk.DoesNotExist:
                return HttpResponseBadRequest()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()

@author_required
@login_required
def suggested_risks(request):
    try:
        review_id = request.GET['review-id']
        suggested_reviews = Review.objects.filter(export_risks=True).exclude(id=review_id)

        context = RequestContext(request, {'suggested_reviews': suggested_reviews})
        return render_to_response('planning/partial_risks_suggested.html', context)
    except Exception as e:
        print e
        return HttpResponseBadRequest()


@author_required
@login_required
def share_risks(request):
    try:
        review_id = request.POST['review-id']
        review = Review.objects.get(pk=review_id)
        review.export_risks = True if not review.export_risks else False
        review.save()
        return HttpResponse()
    except Exception as e:
        print str(e)
        return HttpResponseBadRequest()


'''
    QUALITY ASSESSMENT FUNCTIONS
'''

@author_required
@login_required
def save_imported_quality_assessment(request):
    try:
        review_id = request.POST['review-id']
        exported_review_id = request.POST['exported-review-id']
        review = Review.objects.get(pk=review_id)

        exported_questions = QualityQuestion.objects.filter(review__id=exported_review_id)
        for question in exported_questions:
            imported_question = QualityQuestion(
                                            review=review,
                                            description=question.description
                                        )
            imported_question.save()

            exported_question_answers = question.get_answers()
            for answer in exported_question_answers:
                imported_answer = QualityAnswer(
                                            review=review,
                                            description=answer.description,
                                            weight=answer.weight,
                                            question=imported_question
                                        )
                imported_answer.save()

        return HttpResponse()
    except Exception as e:
        print 'erro ', e
        return HttpResponseBadRequest()

@author_required
@login_required
def add_quality_assessment_question(request):
    try:
        quality_question = QualityQuestion()
        context = RequestContext(request, {'quality_question': quality_question})
        return render_to_response('planning/partial_quality_assessment_question_form.html', context)
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def edit_quality_assessment_question(request):
    try:
        quality_question_id = request.GET['quality-question-id']
        quality_question = QualityQuestion.objects.get(pk=quality_question_id)
        context = RequestContext(request, {'quality_question': quality_question})
        return render_to_response('planning/partial_quality_assessment_question_form.html', context)
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def save_quality_assessment_question(request):
    try:
        description = request.POST['description']
        review_id = request.POST['review-id']
        quality_question_id = request.POST['quality-question-id']

        review = Review.objects.get(pk=review_id)

        if quality_question_id == 'None':
            quality_question = QualityQuestion(review=review)
        else:
            quality_question = QualityQuestion.objects.get(pk=quality_question_id)

        quality_question.description = description
        quality_question.save()

        context = RequestContext(request, {'quality_question': quality_question})
        return render_to_response('planning/partial_quality_assessment_question.html', context)
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def save_quality_assessment_question_order(request):
    try:
        orders = request.POST.get('orders')
        question_orders = orders.split(',')
        for question_order in question_orders:
            if question_order:
                question_id, order = question_order.split(':')
                question = QualityQuestion.objects.get(pk=question_id)
                question.order = order
                question.save()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def remove_quality_assessment_question(request):
    try:
        quality_question_id = request.GET['quality-question-id']
        quality_question = QualityQuestion.objects.get(pk=quality_question_id)
        quality_question.delete()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()

@author_required
@login_required
def suggested_quality_assessment_questions(request):
    try:
        review_id = request.GET['review-id']
        suggested_reviews = Review.objects.filter(export_qualityassessment=True).exclude(id=review_id)
        context = RequestContext(request, {'suggested_reviews': suggested_reviews})
        return render_to_response('planning/partial_quality_assessment_question_suggested.html', context)
    except Exception as e:
        print e
        return HttpResponseBadRequest()

@author_required
@login_required
def share_quality_assessment_questions(request):
    try:
        review_id = request.POST['review-id']
        review = Review.objects.get(pk=review_id)
        review.export_qualityassessment = True if not review.export_qualityassessment else False
        review.save()

        return HttpResponse()
    except:
        return HttpResponseBadRequest()

@author_required
@login_required
def add_quality_assessment_answer(request):
    try:
        quality_question_id = request.GET['quality-question-id']
        quality_answer = QualityAnswer()
        quality_question = QualityQuestion.objects.get(pk=quality_question_id)
        context = RequestContext(request, {'quality_answer': quality_answer, 'quality_question': quality_question})
        return render_to_response('planning/partial_quality_assessment_answer_form2.html', context)
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def edit_quality_assessment_answer(request):
    try:
        quality_answer_id = request.GET['quality-answer-id']
        quality_question_id = request.GET['quality-question-id']

        quality_answer = QualityAnswer.objects.get(pk=quality_answer_id)
        quality_question = QualityQuestion.objects.get(pk=quality_question_id)
        context = RequestContext(request, {'quality_answer': quality_answer, 'quality_question': quality_question})
        return render_to_response('planning/partial_quality_assessment_answer_form.html', context)
    except:
        return HttpResponseBadRequest()

@author_required
@login_required
def edit_quality_assessment_answer2(request):
    try:
        quality_answer_id = request.GET['quality-answer-id']
        quality_question_id = request.GET['quality-question-id']

        quality_answer = QualityAnswer.objects.get(pk=quality_answer_id)
        quality_question = QualityQuestion.objects.get(pk=quality_question_id)
        context = RequestContext(request, {'quality_answer': quality_answer, 'quality_question': quality_question})
        return render_to_response('planning/partial_quality_assessment_answer_form2.html', context)
    except:
        return HttpResponseBadRequest()

@author_required
@login_required
def save_quality_assessment_answer(request):
    try:
        description = request.POST['description']
        weight = request.POST['weight']
        review_id = request.POST['review-id']
        quality_answer_id = request.POST['quality-answer-id']
        quality_question_id = request.POST['quality-question-id']

        weight = weight.replace(',', '.')
        try:
            weight = float(weight)
        except:
            weight = 0.0

        review = Review.objects.get(pk=review_id)
        question = QualityQuestion.objects.get(pk=quality_question_id)

        if quality_answer_id == 'None':
            quality_answer = QualityAnswer(review=review)
        else:
            quality_answer = QualityAnswer.objects.get(pk=quality_answer_id)

        quality_answer.description = description
        quality_answer.weight = weight
        quality_answer.question = question
        quality_answer.save()

        context = RequestContext(request, {'quality_answer': quality_answer, 'quality_question': question})
        return render_to_response('planning/partial_quality_assessment_answer2.html', context)
    except Exception as e:
        print e
        return HttpResponseBadRequest()


@author_required
@login_required
def remove_quality_assessment_answer(request):
    try:
        quality_answer_id = request.GET['quality-answer-id']
        quality_answer = QualityAnswer.objects.get(pk=quality_answer_id)
        quality_answer.delete()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()

@author_required
@login_required
def suggested_quality_assessment_answers(request):
    try:
        review_id = request.GET['review-id']
        suggested_reviews = Review.objects.filter(export_qualityassessment=True).exclude(id=review_id)

        context = RequestContext(request, {'suggested_reviews': suggested_reviews})
        return render_to_response('planning/partial_quality_assessment_answer_suggested.html', context)
    except Exception as e:
        print e
        return HttpResponseBadRequest()


@author_required
@login_required
def add_suggested_answer(request):
    try:
          
        review_id = request.GET['review-id']
        quality_question_id = request.GET['quality-question-id']
        review = Review.objects.get(pk=review_id)
        quality_question = QualityQuestion.objects.get(pk=quality_question_id)
        
       
        #if not quality_question.get_answers():
        html_answers = u''
        for answer, value in QualityAnswer.SUGGESTED_ANSWERS:
            quality_answer = QualityAnswer(review=review, description=answer, weight=value, question=quality_question)
            quality_answer.save()
            html_answers += '''<li id="li-quality-question-{3}-answer-{0}"
                                oid="{0}" data-question-id="{3}" class="list-group-item" style="padding: 3px 3px;" >
                                    <div class="row" id="row-quality-question-{3}-answer-{0}">
             <div class="col-lg-6">
                <small><em>
                    {1}
                </em></small>
            </div>
            <div class="col-lg-3">
                <small><em>
                    {2}
                </em></small>
            </div>
            <div class="col-lg-3">
                <button type="button" class="btn btn-default btn-sm btn-edit-quality-answer" data-question-id="{3}" data-answer-id="{0}">
                    <span class="glyphicon glyphicon-pencil"></span>
                    editar
                </button>
                <button type="button" class="btn btn-default btn-sm btn-remove-quality-answer">
                    <span class="glyphicon glyphicon-trash"></span>
                    remover
                </button>
            </div>
            </div></li>'''.format(quality_answer.id, quality_answer.description.encode('ascii', 'replace').replace('?','&atilde;'), quality_answer.weight, quality_question.id)
        return HttpResponse(html_answers)
        #else:
        #    return HttpResponseBadRequest()
    except Exception as e:
        print 'except ', e
        return HttpResponseBadRequest()



@author_required
@login_required
def calculate_max_score(request):
    try:
        review_id = request.GET['review-id']
        review = Review.objects.get(pk=review_id)
        max_score = review.calculate_quality_assessment_max_score()
        return HttpResponse(max_score)
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def save_cutoff_score(request):
    try:
        review_id = request.GET['review-id']
        cutoff_score = request.GET['cutoff-score']
        review = Review.objects.get(pk=review_id)
        review.quality_assessment_cutoff_score = float(cutoff_score)
        review.save()
        return HttpResponse(_('Cutoff score saved successfully!'))
    except:
        return HttpResponseBadRequest('Invalid value.')


'''
    DATA EXTRACTION FUNCTIONS
'''

@author_required
@login_required
def add_new_data_extraction_field(request):
    field = DataExtractionField()
    context = RequestContext(request, {'field': field})
    return render_to_response('planning/partial_data_extraction_field_form.html', context)


@author_required
@login_required
def edit_data_extraction_field(request):
    field_id = request.GET['field-id']
    field = DataExtractionField.objects.get(pk=field_id)
    context = RequestContext(request, {'field': field})
    return render_to_response('planning/partial_data_extraction_field_form.html', context)


@author_required
@login_required
def save_data_extraction_field(request):
    try:
        review_id = request.POST['review-id']
        description = request.POST['description']
        field_type = request.POST['field-type']
        lookup_values = request.POST['lookup-values']
        field_id = request.POST['field-id']

        if not field_type and not description:
            return HttpResponseBadRequest(_('Description and Type are required fields.'))

        lookup_values = lookup_values.split('\n')
        lookup_values = list(set(lookup_values))

        for i in range(0, len(lookup_values)):
            lookup_values[i] = lookup_values[i].strip()

        review = Review.objects.get(pk=review_id)

        if field_id == 'None':
            field = DataExtractionField(review=review)
        else:
            field = DataExtractionField.objects.get(pk=field_id)
            if field.field_type != field_type:
                try:
                    data_extractions = DataExtraction.objects.filter(field__id=field_id)
                    for data_extraction in data_extractions:
                        data_extraction.value = ''
                        data_extraction.select_values.clear()
                        data_extraction.save()
                except Exception, e:
                    pass

        field.description = description
        field.field_type = field_type
        field.save()

        if field.is_select_field():
            for value in lookup_values:
                if value:
                    lookup_value, created = DataExtractionLookup.objects.get_or_create(field=field, value=value)

            for select_value in field.get_select_values():
                if select_value.value not in lookup_values:
                    select_value.delete()
        else:
            for select_value in field.get_select_values():
                select_value.delete()

        context = RequestContext(request, {'field': field})
        return render_to_response('planning/partial_data_extraction_field.html', context)
    except Exception as e:
        print e
        return HttpResponseBadRequest()


@author_required
@login_required
def save_data_extraction_field_order(request):
    try:
        orders = request.POST.get('orders')
        field_orders = orders.split(',')
        for field_order in field_orders:
            if field_order:
                field_id, order = field_order.split(':')
                field = DataExtractionField.objects.get(pk=field_id)
                field.order = order
                field.save()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()


@author_required
@login_required
def remove_data_extraction_field(request):
    try:
        field_id = request.GET['field-id']
        field = DataExtractionField.objects.get(pk=field_id)
        select_values = field.get_select_values()
        for select_value in select_values:
            select_value.delete()
        field.delete()
        return HttpResponse()
    except:
        return HttpResponseBadRequest()

@author_required
@login_required
def suggested_data_extraction_fields(request):
    try:
        review_id = request.GET['review-id']
        suggested_reviews = Review.objects.filter(export_dataextraction=True).exclude(id=review_id)

        context = RequestContext(request, {'suggested_reviews': suggested_reviews})
        return render_to_response('planning/partial_data_extraction_suggested.html', context)
    except Exception as e:
        print e
        return HttpResponseBadRequest()

@author_required
@login_required
def share_data_extraction_fields(request):
    try:
        review_id = request.POST['review-id']
        review = Review.objects.get(pk=review_id)
        review.export_dataextraction = True if not review.export_dataextraction else False
        review.save()

        if review.export_dataextraction:
            return HttpResponse(_('Data Extraction Fields has been shared!'))

        return HttpResponse(_('Data Extraction Fields has been made private again!'))
    except:
        return HttpResponseBadRequest()

@author_required
@login_required
def setting_pico(request):
    review_id = request.GET['review-id']
    review = Review.objects.get(pk=review_id)
    pico_type = request.GET['pico_type']
    review.pico_type = pico_type
    review.save()
    return render(request, 'planning/protocol.html', { 'review': review })

@author_required
@login_required
def share_pico(request):
    try:
        review_id = request.POST['review-id']
        review = Review.objects.get(pk=review_id)
        review.export_pico = True if not review.export_pico else False
        review.save()
        return HttpResponse(review.export_pico)
    except Exception as e:
        print str(e)
        return HttpResponseBadRequest()

@author_required
@login_required
def suggested_pico(request):
    try:
        review_id = request.GET['review-id']
        suggested_reviews = Review.objects.filter(Q(export_pico=True) | Q(export_protocol=True)).exclude(id=review_id)

        context = RequestContext(request, {'suggested_reviews': suggested_reviews})
        return render_to_response('planning/partial_pico_suggested.html', context)
    except Exception as e:
        print e
        return HttpResponseBadRequest()

@author_required
@login_required
def import_pico(request):
    try:
        review_id = request.GET['review-id']
        review = Review.objects.get(pk=review_id)

        ref_review_id = request.GET['ref-review-id']
        ref_review = Review.objects.get(pk=ref_review_id)

        response = {};

        review.pico_type = ref_review.pico_type
        response['pico_type'] = review.pico_type

        if ref_review.isStudyTypeFree():
            review.pico_text = ref_review.pico_text
            response['pico_text'] = review.pico_text
        else:
            review.population = ref_review.population
            review.intervention = ref_review.intervention
            review.comparison = ref_review.comparison
            review.outcome = ref_review.outcome

            response['population'] = review.population
            response['intervention'] = review.intervention
            response['comparison'] = review.comparison
            response['outcome'] = review.outcome

            if ref_review.isPicoc():
                review.context = ref_review.context
                response['context'] = review.context
            elif ref_review.isPicos():
                review.study_type = ref_review.study_type
                response['study_type'] = review.study_type

        review.save()

        dump = json.dumps(response)
        return HttpResponse(dump, content_type='application/json')
    except Exception as e:
        print str(e)
        return HttpResponseBadRequest()

