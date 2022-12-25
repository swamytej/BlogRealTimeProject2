from django import template
from BlogApp2.models import Post
register = template.Library()

#@register.simple_tag
@register.simple_tag(name='my_tag')
def total_posts():
    return Post.objects.count()

@register.inclusion_tag('BlogApp2/latest_posts.html')
def show_latest_posts(count=2):
    latest_posts=Post.objects.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}


from django.db.models import Count
#@register.assignment_tag
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


