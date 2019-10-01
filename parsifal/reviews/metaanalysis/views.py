# coding: utf-8

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse as r
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.translation import ugettext as _
from django.template import RequestContext
import datetime

from parsifal.reviews.models import *
from parsifal.reviews.decorators import author_required, author_or_visitor_required, visitor_required


@author_or_visitor_required
@login_required
def metaanalysis(request, username, review_name):
    review = get_object_or_404(Review, name=review_name, author__username__iexact=username)
    selected_articles = review.get_accepted_articles().filter(has_empirical_data=True)
    return render(request, 'metaanalysis/metaanalysis_list.html', { 
        'review': review , 
        'selected_articles': selected_articles})


@author_or_visitor_required
@login_required
def articles_metaanalysis(request, username, review_name):
    review = get_object_or_404(Review, name=review_name, author__username__iexact=username)
    selected_articles = review.get_accepted_articles().filter(has_empirical_data=True)
    return render(request, 'metaanalysis/metaanalysis_list.html', { 
        'review': review , 
        'selected_articles': selected_articles})

@login_required
def save_metaanalysis(request):
    try:

        return HttpResponse(_('Your comment have been sended successfully!'))
    except Exception as e:
        print e
        return HttpResponseBadRequest()
    
@author_or_visitor_required
@login_required
def metaanalysis_detailed(request, username, review_name, article_id):
    review = get_object_or_404(Review, name=review_name, author__username__iexact=username)
   
    return render(request, 'metaanalysis/metaanalysis_detailed.html', { 'review': review, 'comment': comment, 'unseen_comments': unseen_comments })
