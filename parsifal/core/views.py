# coding: utf-8

from django.core.urlresolvers import reverse as r
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.html import escape
from django.utils.translation import ugettext as _

from parsifal.activities.models import Activity
from parsifal.blog.models import Entry
from parsifal.reviews.models import Review
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import logging

logger = logging.getLogger('PARSIFAL_LOG')

def get_following_feeds(user):
    feeds = []
    try:
        activities = []
        followers = Activity.objects.filter(to_user=user, activity_type=Activity.FOLLOW)
        for follower_user in followers:
            activities.append(follower_user)
        following = Activity.objects.filter(from_user=user, activity_type=Activity.FOLLOW)
        for following_user in following:
            activities.append(following_user)
            initial_activity = Activity.objects.get(from_user=user, to_user=following_user.to_user, activity_type=Activity.FOLLOW)
            following_user_activities = Activity.objects.filter(from_user=following_user.to_user, activity_type=Activity.FOLLOW, date__gte=initial_activity.date).exclude(to_user=user)
            for activity in following_user_activities:
                activities.append(activity)
        activities.sort(key=lambda a: a.date, reverse=True)
        for activity in activities:
            if activity.from_user == user:
                activity.message = u'<a href="{0}">' + _('You') + ' </a> ' + _('are now following') + ' <a href="{1}">{2}</a>'.format(
                    r('reviews', args=(user.username,)),
                    r('reviews', args=(activity.to_user.username,)),
                    escape(activity.to_user.profile.get_screen_name())
                    )
            else:
                is_following = activity.to_user.profile.get_screen_name()
                if activity.to_user == user:
                    is_following = _(u'you')
                activity.message = u'<a href="{0}">{1}</a> ' + _('is now following') + ' <a href="{2}">{3}</a>'.format(
                    r('reviews', args=(activity.from_user.username,)),
                    escape(activity.from_user.profile.get_screen_name()),
                    r('reviews', args=(activity.to_user.username,)),
                    escape(is_following)
                    )
            feeds.append(activity)
    except Exception, e:
        pass
    return feeds

def home(request):
    if request.user.is_authenticated():
        show_head = True
        user_reviews = request.user.profile.get_reviews()
        invited_reviews = request.user.profile.get_invited_reviews()
        feeds = get_following_feeds(request.user)
        try:
            latest_news = Entry.objects.filter(status=Entry.PUBLISHED).order_by('-start_publication',)[0]
        except:
            latest_news = None
        return render(request, 'core/home.html', {
                'user_reviews': user_reviews,
                'invited_reviews': invited_reviews,
                'feeds': feeds,
                'latest_news': latest_news,
                'show_head' : show_head
            })
    else:
        
        return render(request, 'core/cover.html')
    
@login_required
def leave_review(request):
    review_id = request.POST.get('review-visitor-id')
    review = get_object_or_404(Review, pk=review_id)
    review.visitors.remove(request.user)
    review.save()
    messages.add_message(request, messages.SUCCESS, _('You successfully left the review {0}.').format(review.title))
    return redirect('home')
    
