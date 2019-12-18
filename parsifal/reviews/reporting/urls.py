# coding: utf-8

from django.conf.urls import patterns, url


urlpatterns = patterns('parsifal.reviews.reporting.views',
    url(r'^download_docx/$', 'download_docx', name='download_docx'),
    url(r'^download_xlsx/$', 'download_xlsx', name='download_xlsx')
)
