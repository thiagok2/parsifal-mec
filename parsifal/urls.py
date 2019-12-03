# coding: utf-8

from django.conf.urls import patterns, include, url, i18n
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('parsifal',
    url(r'^i18n/', include('django.conf.urls.i18n'), name='set_language'),
    url(r'^$', 'core.views.home', name='home'),
    
    url(r'^leave_review/$', 'core.views.leave_review', name='leave_review'),
    url(r'^recovery_source/$', 'reviews.settings.views.recovery_source', name='recovery_source'),
    
    url(r'^about/$', TemplateView.as_view(template_name='core/about.html'), name='about'),
    url(r'^signup/$', 'authentication.views.signup', name='signup'),
    url(r'^signin/$', 'authentication.views.signin', name='signin'),
    url(r'^signout/$', 'authentication.views.signout', name='signout'),
    url(r'^reset/$', 'authentication.views.reset', name='reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'authentication.views.reset_confirm', name='password_reset_confirm'),
    url(r'^success/$', 'authentication.views.success', name='success'),
    url(r'^reviews/', include('parsifal.reviews.urls', namespace='reviews')),
    url(r'^activity/', include('parsifal.activities.urls', namespace='activities')),
    url(r'^blog/', include('parsifal.blog.urls', namespace='blog')),
    url(r'^help/', include('parsifal.help.urls', namespace='help')),
    
    #url(r'^library/', include('parsifal.library.urls', namespace='library')),
    url(r'^settings/', include('parsifal.account_settings.urls', namespace='settings')),
    url(r'^review_settings/transfer/$', 'reviews.settings.views.transfer', name='transfer_review'),
    url(r'^review_settings/delete/$', 'reviews.settings.views.delete', name='delete_review'),
    url(r'^review_settings/publish_protocol/$', 'reviews.settings.views.publish_protocol', name='publish_protocol'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sitemap.xml$', TemplateView.as_view(template_name='sitemap.xml', content_type='application/xml')),
    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^(?P<username>[^/]+)/following/$', 'activities.views.following', name='following'),
    url(r'^(?P<username>[^/]+)/followers/$', 'activities.views.followers', name='followers'),
    # Review URLs
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/$', 'reviews.views.review', name='review'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/settings/$', 'reviews.settings.views.settings', name='settings'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/recovery/$', 'reviews.settings.views.recovery', name='recovery'),

    # Review comments
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/comments/$', 'reviews.comments.views.comments', name='comments'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/comments/detailed/(?P<comment_id>[^/]+)/$', 'reviews.comments.views.comment_detailed', name='comment_detailed'),

    # Planning Phase
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/planning/$', 'reviews.planning.views.planning', name='planning'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/planning/protocol/$', 'reviews.planning.views.protocol', name='protocol'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/planning/quality/$', 'reviews.planning.views.quality_assessment_checklist', name='quality_assessment_checklist'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/planning/extraction/$', 'reviews.planning.views.data_extraction_form', name='data_extraction_form'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/planning/risks/$', 'reviews.planning.views.risks_to_review_validity', name='risks_to_review_validity'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/planning/statistical/$', 'reviews.planning.views.statistical_methods_conventions', name='statistical_methods_conventions'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/planning/setup/$', 'reviews.planning.views.search_setup', name='search_setup'),

    # Conducting Phase
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/conducting/$', 'reviews.conducting.views.conducting', name='conducting'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/conducting/search/$', 'reviews.conducting.views.search_studies', name='search_studies'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/conducting/import/$', 'reviews.conducting.views.import_studies', name='import_studies'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/conducting/studies/$', 'reviews.conducting.views.study_selection', name='study_selection'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/conducting/quality/$', 'reviews.conducting.views.quality_assessment', name='quality_assessment'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/conducting/extraction/$', 'reviews.conducting.views.data_extraction', name='data_extraction'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/conducting/analysis/$', 'reviews.conducting.views.data_analysis', name='data_analysis'),

     # Meta Analysis Phase
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/metaanalysis/$', 'reviews.metaanalysis.views.metaanalysis', name='metaanalysis'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/metaanalysis/list$', 'reviews.metaanalysis.views.metaanalysis_list', name='metaanalysis_list'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/metaanalysis/detailed/(?P<article_id>[^/]+)/$', 'reviews.metaanalysis.views.metaanalysis_detailed', name='metaanalysis_detailed'),

    # Reporting Phase
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/reporting/$', 'reviews.reporting.views.reporting', name='reporting'),
    url(r'^(?P<username>[^/]+)/(?P<review_name>[^/]+)/reporting/export/$', 'reviews.reporting.views.export', name='export'),

    url(r'^(?P<username>[^/]+)/$', 'reviews.views.reviews', name='reviews'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
