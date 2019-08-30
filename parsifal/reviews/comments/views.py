# coding: utf-8

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse as r
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.translation import ugettext as _

from parsifal.reviews.models import *
from parsifal.reviews.decorators import author_required, visitor_required

@author_required
@login_required
def comments(request, username, review_name):
    review = get_object_or_404(Review, name=review_name, author__username__iexact=username)
    return render(request, 'comments/comments.html', { 'review': review })


#@visitor_required
@login_required
def save_visitor_comment(request):
    try:
        print 'save'
        review_id = request.POST['review-id']
        comment = request.POST['comment']
        about = request.POST['about']
        user = request.user
        review = Review.objects.get(pk=review_id)

        comment = VisitorComment(review=review, comment=comment, about=about, user=user)
        comment.save()

        return HttpResponse(_('Your comment have been sended successfully!'))
    except Exception as e:
        return HttpResponseBadRequest()
