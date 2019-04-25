from django import template
from friendship.models import Block, Follow

register = template.Library()

@register.simple_tag
def blocked_by(user_blocker, user_blocked):
    blocking = Block.objects.blocking(user_blocker)
    is_blocked = user_blocked in blocking
    return is_blocked

@register.simple_tag
def blocking_list(user):
    blocking = Block.objects.blocking(user)
    return blocking

@register.simple_tag
def following_list(user):
    following = Follow.objects.following(user)
    return following