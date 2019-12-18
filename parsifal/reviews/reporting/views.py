# coding: utf-8

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse as r
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest

from parsifal.reviews.models import *
from parsifal.reviews.decorators import author_required, author_or_visitor_required
from parsifal.reviews.reporting.export import export_review_to_docx, export_review_to_xlsx
from django.utils.translation import ugettext as _

import logging

import xlsxwriter

logger = logging.getLogger('PARSIFAL_LOG')


@author_or_visitor_required
@login_required
def reporting(request, username, review_name):
    return redirect(r('export', args=(username, review_name,)))

@author_or_visitor_required
@login_required
def export(request, username, review_name):
    try:
        review = get_object_or_404(Review, name=review_name, author__username__iexact=username)
        unseen_comments = review.get_visitors_unseen_comments(request.user)

        return render(request, 'reporting/export.html', { 'review': review, 'unseen_comments': unseen_comments })
    except Exception as e:
        logger.exception(request.user.username + ': ' + _('An expected error occurred.') )
        return HttpResponseBadRequest(e)

@author_or_visitor_required
@login_required
def download_docx(request):
    try:
        review_id = request.POST.get('review-id')
        review = get_object_or_404(Review, pk=review_id)
        sections = request.POST.getlist('export')
        document = export_review_to_docx(review, sections, request)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = u'attachment; filename={0}.docx'.format(review.name)
        document.save(response)
        return response
    except Exception as e:
        logger.exception(request.user.username + ': ' + _('An expected error occurred.'))
        return HttpResponseBadRequest(e)

@author_or_visitor_required
@login_required
def download_xlsx(request):
    try:
        review_id = request.POST.get('review-id')
        review = get_object_or_404(Review, pk=review_id)


        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename={0}.xlsx".format(review.name)
        workbook = xlsxwriter.Workbook(response, {'in_memory': True, 'default_date_format':'dd/mm/yyyy'})

        workbook = export_review_to_xlsx(review, workbook)

        return response



    except Exception as e:
        logger.exception(request.user.username + ': ' + _('An expected error occurred.'))
        return HttpResponseBadRequest(e)
