from django.contrib.sitemaps import Sitemap
from .models import Post


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

