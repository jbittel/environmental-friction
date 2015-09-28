from __future__ import unicode_literals

import pytest

from .factories import PostFactory


@pytest.mark.django_db
@pytest.mark.parametrize('post__title', ['First Post'])
def test_post_slug(post):
    assert post.slug == 'first-post'
