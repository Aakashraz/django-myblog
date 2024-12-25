import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post


# we have defined a feed by subclassing the Feed class of the syndication
# framework. The title, link, and description attributes correspond to the <title>, <link>, and
# <description> RSS elements, respectively.
class LatestPostsFeed(Feed):
    title = 'My Blog'
    link = reverse_lazy('blog:post_list')
    description = 'New posts of my blog.'

    # The items() method retrieves the objects to be included in the feed.
    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    # In the item_description() method, we use the markdown() function to convert Markdown content
    # to HTML and the truncatewords_html() template filter function to cut the description of posts after
    # 30 words, avoiding unclosed HTML tags.
    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item):
        return item.publish

#   The item_title(), item_description(), and item_pubdate() methods will receive each object
#   returned by items() and return the title, description, and publication date for each item.
