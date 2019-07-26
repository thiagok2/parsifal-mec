from django import template
from parsifal.reviews.models import Review

register = template.Library()

@register.filter
def is_visitor(user, review):
    review = Review.objects.get(pk=review.id)
    if review.export_protocol and not user == review.author and not user in review.co_authors.all():
        return True

    for visitor in review.visitors.all():
        if user.id == visitor.id:
            return True
    return False
