from django.contrib.sitemaps import Sitemap
from .models import Post
from taggit.models import Tag
from django.urls import reverse


# To include URLs for tag-filtered views in your sitemap
class TagSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        # get all tags used in the blog
        return Tag.objects.all()

    # In a Django Sitemap class, the location() method is responsible for generating
    # the URL for each item returned by the items() method.
    def location(self, obj):
        # generate the URL for a tag-filtered view
        return reverse('blog:post_list_by_tag', args=[obj.slug])


class PostSitemap(Sitemap):
    changefreq = 'weekly'       # How often posts change
    priority = 0.9              # Importance (0.0 to 1.0)

    # method for including which objects to include
    def items(self):
        return Post.published.all()

    # Last modified date
    def lastmod(self, obj):
        return obj.updated_on
        # return obj.author

        # if used the: return obj.author, it causes error.
        # The error occurs because the lastmod method must return a date/timestamp, not an author object.
        # The sitemap needs dates to show when content was last modified.

