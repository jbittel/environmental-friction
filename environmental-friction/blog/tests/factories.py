from __future__ import unicode_literals

from datetime import timedelta

from django.contrib.auth.models import User
from django.utils.timezone import now

import factory

from blog.models import Post


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.LazyAttribute(lambda o: o.first_name.lower())
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password')
    last_login = now()


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Faker('sentence')
    body = factory.Faker('paragraph')
    author = factory.SubFactory(AuthorFactory)
    publish = now()


class UnpublishedPostFactory(PostFactory):
    publish = now() + timedelta(hours=1)
