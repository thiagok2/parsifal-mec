from django import template
from parsifal.reviews.models import Article, ArticleEvaluation

register = template.Library()

@register.assignment_tag
def get_user_article_evaluation(article, user_id):
    status = Article.objects \
                .get(id=article.id) \
                .get_user_evaluation(user_id=user_id)

    return status
