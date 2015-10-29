from django.conf.urls import patterns
from django.conf.urls import url

from .views import PostList
from .views import PostDetail


urlpatterns = patterns('',
    url(r'^$', PostList.as_view(), name='post-list'),
    url(r'^(?P<pk>\w+)(?:/(?P<slug>[\w\-]*))?$', PostDetail.as_view(), name='post-detail'),
)
