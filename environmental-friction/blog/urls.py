from django.conf.urls import url

from . import views
from .feeds import AtomFeed
from .feeds import RSSFeed


app_name = 'blog'

urlpatterns = [
    url(r'^$', views.PostList.as_view(), name='list'),
    url(r'^write/$', views.Write.as_view(), name='write'),
    url(r'^write/(?P<pk>\d+)/$', views.EditPost.as_view(), name='edit'),
    url(r'^feed/atom/$', AtomFeed(), name='atom'),
    url(r'^feed/rss/$', RSSFeed(), name='rss'),
    url(r'^(?P<pk>\w+)(?:/(?P<slug>[\w\-]*))?$', views.PostDetail.as_view(), name='detail'),
]
