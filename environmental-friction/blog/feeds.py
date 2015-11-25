from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse_lazy
from django.utils.feedgenerator import Atom1Feed

from .models import Post
from .templatetags.markup import markup


class RSSFeed(Feed):
    title = Site.objects.get_current().name
    link = reverse_lazy('blog:list')
    feed_url = reverse_lazy('blog:rss')
    description = 'Changing habits to transform communities'

    def items(self):
        return Post.objects.published()[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return markup(item.body)


class AtomFeed(RSSFeed):
    feed_type = Atom1Feed
    feed_url = reverse_lazy('blog:atom')
    subtitle = RSSFeed.description
