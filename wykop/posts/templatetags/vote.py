from django import template
from wykop.posts.models import Vote

register = template.Library()

@register.simple_tag(takes_context=True)
def user_vote_for_post(context):
    user = context['user']
    post = context['post']

    if not user.is_authenticated:
        return 0

    try:
        return post.votes.get(user=user).value
    except Vote.DoesNotExist:
        return 0
