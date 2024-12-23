from django import template
from django.db.models import Count
import markdown
from django.utils.safestring import mark_safe

from ..models import Post


# Each module that contains template tags needs to define a variable called register to be a valid tag
# library. This variable is an instance of template.Library, and it’s used to register the template tags
# and filters of the application
register = template.Library()


# We have added the @register.simple_tag decorator to the function, to register it as a simple tag.
# Django will use this function's name as the tag name.
# If you want to register it using a different name, you can do so by specifying a name attribute,
# such as @register.simple_tag(name='my_tag')
@register.simple_tag
def total_posts():
    return Post.published.count()


# The line @register.inclusion_tag('blog/post/latest_posts.html') is telling Django "Hey, I want to create
# a new template tag, and when I use it, please use this HTML file (latest_posts.html) to display the results."
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    # [:count] takes only the number of posts you specified (like saying "give me the first 5")
    return {'latest_posts': latest_posts}


# to use this in your templates, you could write something like:
# {% show_latest_posts %} --> Shows % posts
# {% show_latest_posts 3 %} --> Shows 3 posts


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]
    # This query is doing several things in sequence:
    #
    # Post.published starts with all your published posts
    # .annotate(total_comments=Count('comments')) adds a new calculated field to each post that counts how many
    # comments it has. Think of it like adding a sticky note to each post with its comment count.
    # .order_by('-total_comments') sorts the posts by their comment count, with the minus sign meaning
    # "highest to lowest" (like arranging posts from most commented to least commented)
    # [:count] takes just the top few posts based on the count parameter we specified


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

# The function markdown_format(text) takes the raw text (containing Markdown syntax) and:
#
# Uses markdown.markdown(text) to convert Markdown to HTML
# Wraps with mark_safe() to tell Django this HTML is safe to render
# Returns the safe HTML
#
# This lets you write blog posts in Markdown and automatically convert them to properly
# formatted HTML in your templates using {{ post.body|markdown }}.

# NOTE
# In Django, HTML content is escaped by default for security. Use mark_safe cautiously,
# only on content you control. Avoid using mark_safe on any content submitted by
# non-staff users to prevent security vulnerabilities.
