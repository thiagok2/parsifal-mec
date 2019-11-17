# coding: utf-8
import json

from django.core.urlresolvers import reverse as r
from django.template.defaultfilters import slugify, nan
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, get_object_or_404, render
from django.template import RequestContext
from django.utils.html import escape
from django.views.decorators.http import require_POST
from django.core.mail import EmailMultiAlternatives

from parsifal.reviews.models import Review, Article, Tag, Invite, Question, Keyword, SearchSession, SelectionCriteria, QualityAnswer, QualityQuestion, Risk,DataExtractionField, DataExtractionLookup
from parsifal.reviews.decorators import main_author_required, author_required, author_or_visitor_required
from parsifal.reviews.forms import CreateReviewForm, ReviewForm

from django.utils.translation import ugettext as _
from decouple import config
from django.db import connection
from django.db import transaction


def reviews(request, username):
    user = get_object_or_404(User, username__iexact=username)
    followers = user.profile.get_followers()
    is_following = False
    if request.user in followers:
        is_following = True

    followers_count = user.profile.get_followers_count()
    following_count = user.profile.get_following_count()

    user_reviews = user.profile.get_reviews()

    context = RequestContext(request, {
        'user_reviews': user_reviews,
        'page_user': user,
        'is_following': is_following,
        'following_count': following_count,
        'followers_count': followers_count
        })
    return render_to_response('reviews/reviews.html', context)

@login_required
def new(request):
    if request.method == 'POST':
        form = CreateReviewForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user

            name = slugify(form.instance.title)
            unique_name = name
            i = 0
            while Review.objects.filter(name=unique_name, author__username=request.user.username):
                i = i + 1
                unique_name = u'{0}-{1}'.format(name, i)
            form.instance.name = unique_name
            review = form.save()
            messages.success(request, _('Review') + ' criada com sucesso.')
            return redirect(r('review', args=(review.author.username, review.name)))
    else:
        form = CreateReviewForm()
    return render(request, 'reviews/new.html', { 'form': form })

@login_required
@author_or_visitor_required
def review(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username__iexact=username)
    unseen_comments = review.get_visitors_unseen_comments(request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save()
            messages.success(request, _(u'Review') +' foi criada com sucesso.')
            return redirect(r('review', args=(review.author.username, review.name)))
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/review.html', {
            'review': review,
            'form': form,
            'unseen_comments': unseen_comments
            })


@main_author_required
@login_required
@require_POST
def add_author_to_review(request):
    emails = request.POST.getlist('users')
    review_id = request.POST.get('review-id')
    review = get_object_or_404(Review, pk=review_id)
    authors_added = []
    authors_invited = []

    inviter_name = request.user.profile.get_screen_name()

    for email in emails:
        try:
            user = User.objects.get(email__iexact=email)
            if user.id != review.author.id:
                authors_added.append(user.profile.get_screen_name())
                review.visitors.remove(user)
                review.co_authors.add(user)
        except User.DoesNotExist:
            authors_invited.append(email)

            for author in authors_invited:
                save_user_invited_to_review(review_id, author, 'co_author')

            subject = _('{0} wants to add you as co-author on the systematic literature review {1}').format(inviter_name, review.title)
            from_email = _('{0} via Parsifal <qeed-suporte@nees.com.br>').format(inviter_name)

            text_content = _('Hi {0}, {1} invited you to a Parsifal Systematic Literature Review called "{2}". View the review at https://qeed.nees.com.br/{3}/{4}/').format(email, inviter_name, review.title, request.user.username, review.name)

            html_content = _('<p>Hi {0},</p><p>{1} invited you to a Parsifal Systematic Literature Review called "{2}".</p><p>View the review at https://qeed.nees.com.br/{3}/{4}/</p><p>Sincerely,</p><p>The Parsifal Team</p>').format(email, inviter_name, review.title, request.user.username, review.name)

            msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

    review.save()

    if not authors_added and not authors_invited:
        messages.info(request, _('No author invited or added to the review. Nothing really changed.'))

    if authors_added:
        messages.success(request, _('The authors {0} were added successfully.').format(u', '.join(authors_added)))

    if authors_invited:
        messages.success(request, _('{0} were invited successfully.').format(u', '.join(authors_invited)))

    return redirect(r('review', args=(review.author.username, review.name)))

@author_required
@login_required
@require_POST
def add_visitor_to_review(request):
    emails = request.POST.getlist('visitors')
    review_id = request.POST.get('review-id')
    review = get_object_or_404(Review, pk=review_id)

    visitors_added = []

    visitors_invited = []

    inviter_name = request.user.profile.get_screen_name()

    for email in emails:
        try:
            user = User.objects.get(email__iexact=email)
            if user.id != review.author.id and not review.is_author_or_coauthor(user) and not review.is_visitors(user):
                visitors_added.append(user.profile.get_screen_name())
                review.visitors.add(user)
        except User.DoesNotExist:
            visitors_invited.append(email)

            for visitor in visitors_invited:
                save_user_invited_to_review(review_id, visitor, 'visitor')

            subject = _('{0} wants to add you as visitor on the systematic literature review {1}').format(inviter_name, review.title)
            from_email = _('{0} via Parsifal <qeed-suporte@nees.com.br>').format(inviter_name)

            text_content = _('Hi {0}, {1} invited you to a Parsifal Systematic Literature Review called "{2}".View the review at https://qeed.nees.com.br/{3}/{4}/').format(email, inviter_name, review.title, request.user.username, review.name)

            html_content = _('<p>Hi {0},</p><p>{1} invited you to a Parsifal Systematic Literature Review called "{2}".</p><p>View the review at https://qeed.nees.com.br/{3}/{4}/</p><p>Sincerely,</p><p>The Parsifal Team</p>').format(email, inviter_name, review.title, request.user.username, review.name)

            msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

    review.save()

    if not visitors_added and not visitors_invited:
        messages.info(request, _('No visitor invited or added to the review. Nothing really changed.'))

    if visitors_added:
        messages.success(request,  _('The visitor {0} were added successfully.').format(u', '.join(visitors_added)))

    if visitors_invited:
        messages.success(request, _('{0} were invited successfully.').format(u', '.join(visitors_invited)))

    return redirect(r('review', args=(review.author.username, review.name)))

@main_author_required
@login_required
@require_POST
def remove_author_from_review(request):
    try:
       
        author_id = request.POST.get('co-author-id')
        review_id = request.POST.get('review-id')
        update_status = request.POST.get('update-status')
        author = User.objects.get(pk=author_id)
        review = Review.objects.get(pk=review_id)
        
        evaluations = review.get_user_evaluation(user_id=author_id)
        
        review.co_authors.remove(author)
        review.save()
        
        messages.success(request, _('The author were removed successfully.'))
        
        if update_status == "true":
            update_article_in_wating_conflict(review)
            messages.success(request, _('The evaluations in articles selection have been updated.'))
        
            
        return redirect(r('review', args=(review.author.username, review.name)))
    except Exception, e:
        print 'ERROR:'+str(e)
        messages.error(request, _('An expected error occurred.') +'ERROR:'+ str(e))
        return HttpResponseBadRequest()
    
@main_author_required
@login_required
@require_POST
def update_status_article_unique_author(request):
    try:
        review_id = request.POST.get('review-id')
        review = Review.objects.get(pk=review_id)
        
        update_article_in_wating_conflict(review)
        
        messages.success(request, _('The status of articles have been updated.'))
        
        return redirect(r('review', args=(review.author.username, review.name)))
    except Exception, e:
        print 'ERROR:'+str(e)
        messages.error(request, _('An expected error occurred.') +'ERROR:'+ str(e))
        return HttpResponseBadRequest()
    

def update_article_in_wating_conflict(review):
    if review.co_authors.count() == 0:
        articles_filter = (article for article in review.get_source_articles().filter( Q(status=Article.WAITING) | Q(status=Article.CONFLICT) ) if article.get_evaluations().count()>0)
        for article in articles_filter:
            evaluations = article.get_evaluations()
            if evaluations.count() == 1 and article.status == Article.WAITING:
               # tem avaliacao do unico autor disponivel, entao nao precisa esperar
               article.status = evaluations[0].status
               article.save()
            elif evaluations.count() > 1 and article.status == Article.CONFLICT: #ha conflito, remove a avaliacao do excluido e considera a avaliacao do outro autor
                for evaluation in evaluations:
                    if review.is_author_or_coauthor( evaluation.user ):
                        article.status = evaluation.status
                        article.save()
                    else: #evaluation.user_id == author_id
                        evaluation.delete()
    

def save_user_invited_to_review(review_id, email, invite_type):
    try:
        review = Review.objects.get(pk=review_id)
        invite = Invite(review=review)
        invite.email = email
        invite.invite_type = invite_type
        invite.save()
        return HttpResponse()
    except Exception, e:
        print e
        messages.error(request, _('An expected error occurred.') + str(e))
        return HttpResponseBadRequest()

@main_author_required
@login_required
@require_POST
def remove_visitor_from_review(request):
    try:
        visitor_id = request.POST.get('user-id')
        review_id = request.POST.get('review-id')
        print 'visitor ', visitor_id
        print 'reid ', review_id
        visitor = User.objects.get(pk=visitor_id)
        review = Review.objects.get(pk=review_id)
        review.visitors.remove(visitor)
        review.save()
        return HttpResponse()
    except Exception, e:
        print e
        messages.error(request, _('An expected error occurred.') + str(e))
        return HttpResponseBadRequest()

@author_required
@login_required
def leave(request):
    review_id = request.POST.get('review-id')
    review = get_object_or_404(Review, pk=review_id)
    review.co_authors.remove(request.user)
    review.save()
    update_article_in_wating_conflict(review)
    messages.add_message(request, messages.SUCCESS, _('You successfully left the review {0}.').format(review.title))
    messages.add_message(request, messages.SUCCESS, _('The evaluations of articles already made for you will be kept.'))
    return redirect('/' + request.user.username + '/')

@author_required
@login_required
def save_description(request):
    try:
        review_id = request.POST['review-id']
        description = request.POST['description']
        review = Review.objects.get(pk=review_id)
        if len(description) > 500:
            return HttpResponseBadRequest(_('The review description should not exceed 500 characters. The given description have %s characters.') % len(description))
        else:
            review.description = description
            review.save()
            return HttpResponse(_('Your review has been saved successfully!'))
    except Exception, e:
        print e
        messages.error(request, _('An expected error occurred.') + str(e))
        return HttpResponseBadRequest()

'''
    REVIEW TAG FUNCTIONS
'''

@author_required
@login_required
def save_tag(request):
    '''
        Function used via Ajax request only.
        This function takes a review tag form and save on the database
    '''
    try:
        review_id = request.POST['review-id']
        tag_id = request.POST['tag-id']
        description = request.POST['description']
        review = Review.objects.get(pk=review_id)
        try:
            tag = Tag.objects.get(pk=tag_id)
        except:
            tag = Tag(review=review)
        tag.tag = description[:300]
        tag.save()
        tag_json = { 'id': tag.id, 'tag': tag.tag }
        return JsonResponse(tag_json, safe=False)
    except Exception, e:
        print e
        messages.error(request, _('An expected error occurred.') + str(e))
        return HttpResponseBadRequest()

@author_or_visitor_required
@login_required
def load_tags(request):
    '''
        Function used via Ajax request only.
        This functions load tags to the review.
    '''
    try:
        review_id = request.GET['review-id']
        tags_list = []
        tags = Tag.objects.filter(review__id=review_id)
        for tag in tags:
            tags_list.append({
                'id': tag.id,
                'tag': tag.tag
            })
        return JsonResponse(tags_list, safe=False)
    except Exception, e:
        print e
        messages.error(request, _('An expected error occurred.') + str(e))
        return HttpResponseBadRequest()

@author_required
@login_required
def remove_tag(request):
    '''
        Function used via Ajax request only.
        This function removes a secondary tag from the review.
    '''
    try:
        review_id = request.POST['review-id']
        tag_id = request.POST['tag-id']
        if tag_id != 'None':
            try:
                tag = Tag.objects.get(pk=tag_id)
                tag.delete()
            except Tag.DoesNotExist:
                return HttpResponseBadRequest()
        return HttpResponse()
    except Exception, e:
        print e
        messages.error(request, _('An expected error occurred.') + str(e))
        return HttpResponseBadRequest()

@login_required
def published_protocols(request):
    '''
        Function used via Ajax request only.
        This function get published protocols from the others review.
    '''
    try:
        review_id = request.GET['review-id']

        print(review_id)
        published_protocols = Review.objects.filter(export_protocol=True).exclude(id=review_id)

        context = RequestContext(request, {'published_protocols': published_protocols})
        return render_to_response('reviews/partial_published_protocols.html', context)
    except Exception as e:
        print e
        messages.error(request, _('An expected error occurred.') + str(e))
        return HttpResponseBadRequest()

@login_required
def import_protocol(request):
    '''
        Function used via Ajax request only.
        This function import protocol to review.
    '''

    try:
        review_id = request.GET['review-id']
        review = Review.objects.get(pk=review_id)

        protocolId = request.GET['protocolId']
        protocol = Review.objects.get(pk=protocolId)

        importDetail = request.GET['importDetail']
        importProtocol = request.GET['importProtocol']
        importChecklist = request.GET['importChecklist']
        importRisks = request.GET['importRisks']
        importDataExtraction = request.GET['importDataExtraction']
        #clearFiedls = request.GET['clearFiedls']

        if importDetail:
            review.description = protocol.description

            Tag.objects.filter(review_id=review_id).delete()
            for protocolTag in Tag.objects.filter(review__id=protocolId):
                newTag = Tag(tag=protocolTag.tag, review = review)
                newTag.save()

        if importProtocol:
            review.objective = protocol.objective
            review.population = protocol.population
            review.intervention = protocol.intervention
            review.comparison = protocol.comparison
            review.outcome = protocol.outcome
            review.context = protocol.context

            Question.objects.filter(review__id=review_id).delete()
            for protocolQ in Question.objects.filter(review__id=protocolId):
                newQ = Question(question=protocolQ.question, order = protocolQ.order, review = review)
                newQ.save();

            Keyword.objects.filter(review__id=review_id).delete()
            for protocolKey in Keyword.objects.filter(review__id=protocolId, synonym_of__isnull=True):
                newKey = Keyword(description = protocolKey.description, review = review, related_to = protocolKey.related_to )
                newKey.save()

                for protocolSyn in protocolKey.get_synonyms():
                    newSyn = Keyword(description = protocolSyn.description, review = review, synonym_of = newKey)
                    newSyn.save()

                newKey.save()

            SearchSession.objects.filter(review__id=review_id, source=None).delete()
            protocolSS = SearchSession.objects.filter(review__id=protocolId, source=None)[:1].get()
            newSearchSession = SearchSession(search_string = protocolSS.search_string,review = review, version = 1)
            newSearchSession.save()

            review.sources.clear()
            for protocolSource in protocol.sources.all():
                review.sources.add(protocolSource)
                review.save()

            SelectionCriteria.objects.filter(review__id=review_id).delete()
            for protocolCriteria in SelectionCriteria.objects.filter(review__id=protocolId):
                newCriteria = SelectionCriteria(review = review, criteria_type = protocolCriteria.criteria_type, description = protocolCriteria.description)
                newCriteria.save()

        if importChecklist:
            QualityQuestion.objects.filter(review__id=review_id).delete()
            for protocol_aq in protocol.get_quality_assessment_questions():
                newAssQuestion = QualityQuestion(review = review, description = protocol_aq.description, order = protocol_aq.order)
                newAssQuestion.save()

            QualityAnswer.objects.filter(review__id=review_id).delete()
            for protocol_aw in protocol.get_quality_assessment_answers():
                newAssQuestion = QualityAnswer(review = review, description = protocol_aw.description, weight = protocol_aw.weight)
                newAssQuestion.save()

            review.quality_assessment_cutoff_score = protocol.quality_assessment_cutoff_score

        if importRisks:
            Risk.objects.filter(review__id=review_id).delete()
            for protocol_risk in protocol.get_risks():
                newRisk = Risk(review = review, risk = protocol_risk.risk)
                newRisk.save()

        if importDataExtraction:
                DataExtractionField.objects.filter(review__id=review_id).delete()

                for protocol_df in protocol.get_data_extraction_fields():
                    new_data_field = DataExtractionField(review = review, description = protocol_df.description,
                                                         field_type = protocol_df.field_type, order = protocol_df.order)
                    new_data_field.save()

                    for protocol_df_value in protocol_df.get_select_values():
                        new_df_value = DataExtractionLookup(field = new_data_field, value = protocol_df_value.value)
                        new_df_value.save()

        review.save()
        return HttpResponse()

    except Exception as e:
        print e
        return HttpResponseBadRequest()

def explorer(request):
    public_reviews = Review.objects.filter(export_protocol=True).order_by('create_date', 'title')[:25]
    context = RequestContext(request, {
       'reviews': public_reviews
    })
    return render_to_response('reviews/explorer.html', context)

def search(request):
    q = request.GET['q']
    public_reviews = Review.objects.filter(export_protocol=True, title__icontains=q).order_by('create_date', 'title')[:25]
    context = RequestContext(request, {
       'reviews': public_reviews,
       'q': q

    })
    return render_to_response('reviews/explorer.html', context)

@author_required
@login_required
def get_review_info(request):
    
    try:
        review_id = request.GET['review-id']
        co_author_id = request.GET['co-author-id']
        co_author = User.objects.get(pk=co_author_id)
        review = Review.objects.get(pk=review_id)
        
        evaluations = review.get_user_evaluation(user_id=co_author.id)
        co_authors_count = review.co_authors.count()
        response = {}
        
        response['review'] = review.name
        #response['evaluations'] = evaluations
        response['evaluations_count'] = evaluations.count()
        response['co_authors_count'] = co_authors_count
        
        
        dump = json.dumps(response)
        return HttpResponse(dump, content_type='application/json')
        
    except Exception as e:
        print str(e)
        return HttpResponseBadRequest()
        
