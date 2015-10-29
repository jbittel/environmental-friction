from __future__ import unicode_literals

import base32_crockford as b32
import pytest

from blog.models import Post
from .factories import PostFactory
from .factories import UnpublishedPostFactory


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize('post__title', ['First Post'])
def test_post_slug(post):
    assert post.slug == 'first-post'


@pytest.mark.parametrize('post__title', ['First Post'])
def test_post_absolute_url(post):
    assert post.get_absolute_url() == '/%s/first-post' % b32.encode(post.pk)


def test_published_posts():
    PostFactory()
    UnpublishedPostFactory()

    assert Post.objects.count() == 2
    assert Post.objects.published().count() == 1
