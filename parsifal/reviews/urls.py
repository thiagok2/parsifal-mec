# coding: utf-8

from django.conf.urls import patterns, include, url


urlpatterns = patterns('parsifal.reviews.views',
    url(r'^new/$', 'new', name='new'),
    url(r'^get_review_info/$', 'get_review_info', name='get_review_info'),
    url(r'^add_author/$', 'add_author_to_review', name='add_author_to_review'),
    url(r'^add_visitor/$', 'add_visitor_to_review', name='add_visitor_to_review'),
    url(r'^remove_author/$', 'remove_author_from_review', name='remove_author_from_review'),
    url(r'^remove_visitor/$', 'remove_visitor_from_review', name='remove_visitor_from_review'),
    url(r'^save_description/$', 'save_description', name='save_description'),
    url(r'^leave/$', 'leave', name='leave'),
    url(r'^save_tag/$', 'save_tag', name='save_tag'),
    url(r'^load_tags/$', 'load_tags', name='load_tags'),
    url(r'^remove_tag/$', 'remove_tag', name='remove_tag'),
    url(r'^planning/', include('parsifal.reviews.planning.urls', namespace='planning')),
    url(r'^conducting/', include('parsifal.reviews.conducting.urls', namespace='conducting')),
    url(r'^reporting/', include('parsifal.reviews.reporting.urls', namespace='reporting')),
    url(r'^comments/', include('parsifal.reviews.comments.urls', namespace='comments')),
    url(r'^metaanalysis/', include('parsifal.reviews.metaanalysis.urls', namespace='metaanalysis')),

    url(r'^published_protocols/$', 'published_protocols', name='published_protocols'),
    url(r'^import_protocol/$', 'import_protocol', name='import_protocol'),

    url(r'^explorer/$', 'explorer', name='explorer'),
    url(r'^search/$', 'search', name='search'),

)
