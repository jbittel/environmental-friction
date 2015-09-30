from django.test import Client

import pytest

from .factories import UnpublishedPostFactory


pytestmark = pytest.mark.django_db


def test_post_list(post):
    c = Client()
    response = c.get('/')
    assert response.status_code == 200


def test_post_detail(post):
    c = Client()
    response = c.get(post.get_absolute_url())
    assert response.status_code == 200


def test_unpublished_post_detail():
    post = UnpublishedPostFactory()
    c = Client()
    response = c.get(post.get_absolute_url())
    assert response.status_code == 404


def test_invalid_post_detail():
    c = Client()
    response = c.get('/A/invalid-post')
    assert response.status_code == 404
