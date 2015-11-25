from django.conf.urls import url

from .feeds import AtomFeed
from .feeds import RSSFeed
from .views import PostList
from .views import PostDetail


urlpatterns = [
    url(r'^$', PostList.as_view(), name='list'),
    url(r'^feed/atom/$', AtomFeed(), name='atom'),
    url(r'^feed/rss/$', RSSFeed(), name='rss'),
    url(r'^(?P<pk>\w+)(?:/(?P<slug>[\w\-]*))?$', PostDetail.as_view(), name='detail'),
]
