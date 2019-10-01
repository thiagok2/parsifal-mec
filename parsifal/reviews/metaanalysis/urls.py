# coding: utf-8

from django.conf.urls import patterns, include, url

urlpatterns = patterns('parsifal.reviews.metaanalysis.views',
    url(r'^save_metaanalysis/$', 'save_metaanalysis', name='save_metaanalysis'),
)
