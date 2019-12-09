# coding: utf-8

from django.core.urlresolvers import reverse as r
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST

from parsifal.reviews.models import Review, Article, Source
from parsifal.reviews.decorators import main_author_required
from parsifal.reviews.settings.forms import ReviewSettingsForm

from django.utils.translation import ugettext as _
import logging

logger = logging.getLogger('PARSIFAL_LOG')

@main_author_required
@login_required
def settings(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username__iexact=username)
    if request.method == 'POST':
        form = ReviewSettingsForm(request.POST, instance=review)
        if form.is_valid():
            name = slugify(form.instance.name)
            unique_name = name
            if unique_name != review_name:
                i = 0
                while Review.objects.filter(name=unique_name, author__username=review.author.username):
                    i = i + 1
                    unique_name = u'{0}-{1}'.format(name, i)
            form.instance.name = unique_name
            review = form.save()
            messages.success(request, _('Review was saved successfully.'))
            return redirect(r('settings', args=(review.author.username, unique_name)))
    else:
        form = ReviewSettingsForm(instance=review)
    return render(request, 'settings/review_settings.html', { 
            'review': review,
            'form': form
            })


@main_author_required
@login_required
def transfer(request):
    try:
        review_id = request.POST['review-id']
        transfer_user_username = request.POST['transfer-user']
        review = Review.objects.get(pk=review_id)
        try:
            transfer_user = User.objects.get(username=transfer_user_username)
        except Exception, e:
            messages.warning(request, _('User not found.'))
            return redirect('settings', review.author.username, review.name)

        current_user = request.user
        if current_user != transfer_user:
            if transfer_user in review.co_authors.all():
                review.co_authors.remove(transfer_user)
            review.author = transfer_user
            review.co_authors.add(current_user)
            review.save()
            logger.info('The review ' + review.to_string() + ' was transfered from  ' + current_user.username + ' to ' + review.author.username)
            return redirect('review', review.author.username, review.name)
        else:
            messages.warning(request, _('Hey! You can\'t transfer the review to yourself.'))
            return redirect('settings', review.author.username, review.name)

    except Exception, e:
        return HttpResponseBadRequest(_('Something went wrong.'))

def publish_protocol(request):
    review_id = request.POST['review-id']
    review = Review.objects.get(pk=review_id)
    review.export_protocol = True if not review.export_protocol else False
    review.save()
    logger.info(review.author.username + ' published the protocol from review ' + review.to_string() )
    return redirect('settings', review.author.username, review.name)

@main_author_required
@login_required
@require_POST
def delete(request):
    review_id = request.POST.get('review-id')
    review = Review.objects.get(pk=review_id)
    username = review.author.username
    sources = review.sources.all()
    for source in sources:
        if not source.is_default:
            review.sources.remove(source)
            source.delete()
    logger.info(username + ' deleted the review ' + review.to_string() )
    review.delete()
    messages.success(request, _('The review was deleted successfully.'))
    return redirect(r('reviews', args=(review.author.username,)))

@main_author_required
@login_required
def recovery(request, username, review_name):
    review = Review.objects.get(name=review_name, author__username__iexact=username)
    source_deleteds = Source.objects.all_with_deleted().filter(deleted__isnull = False)
    
    sources_review = []
    for source in source_deleteds:
        #print source.to_string()
        count = source.get_articles_count_with_deleted(review.id)
        if count > 0 and source.deleted:
            sources_review.append(source)
            #print 'add ' + source.to_string()
    
    
    articles_deleteds = Article.objects.all_with_deleted().filter(review__id=review.id).filter(deleted__isnull = False)
   
    for article in articles_deleteds:
        if not article.source in sources_review:
            sources_review.append(article.source)
        
    
    context = RequestContext(request, {
            'review': review,
            'sources_review': sources_review})
        
    return render_to_response('settings/recovery.html', context)

@main_author_required
@login_required
def recovery_source(request):
    review_id = request.POST.get('review-id')
    review = Review.objects.get(pk=review_id)
    
    source_id = request.POST.get('source-id')
    source = Source.objects.all_with_deleted().get(pk=source_id)
    
    review.sources.add(source)
    if(source.deleted):
        source.undelete()
    elif(source.is_default):
        Article.objects.all_with_deleted().filter(review__id=review.id, source__id = source.id).filter(deleted__isnull = False).undelete()
    
    
    source.get_deleted_search_session().filter(deleted__isnull = False).undelete()
    
    unseen_comments = review.get_visitors_unseen_comments(request.user)
    messages.success(request, _('Source was restored successfully.'))
    
    return render(request, 'planning/protocol.html', { 'review': review, 'unseen_comments': unseen_comments })
