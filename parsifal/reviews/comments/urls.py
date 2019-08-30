# coding: utf-8

from django.conf.urls import patterns, include, url

urlpatterns = patterns('parsifal.reviews.comments.views',
    url(r'^save_visitor_comment/$', 'save_visitor_comment', name='save_visitor_comment'),
)
