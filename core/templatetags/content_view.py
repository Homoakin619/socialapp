from django import template
from django.shortcuts import get_object_or_404

from core.models import Post


register = template.Library()

@register.filter
def get_content(input):
    post = get_object_or_404(Post,pk=input.post_id)
    if input.notification_type == 'POST':
        content = f"{input.post_creator.username} just made a post '{post.content}' "
        return content
    else:
        content = f'{input.post_creator.username} commented on your post  "{post.content}"'
        return content