from django import template
from friendship.models import Block

register = template.Library()

@register.simple_tag
def blocked_by(user_blocker, user_blocked):
    blocking = Block.objects.blocking(user_blocker)
    is_blocked = user_blocked in blocking
    return is_blocked