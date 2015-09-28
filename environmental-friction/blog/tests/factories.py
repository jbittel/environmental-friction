from __future__ import unicode_literals

from datetime import timedelta

from django.contrib.auth.models import User
from django.utils.timezone import now

import factory
from faker import Factory as FakerFactory

from blog.models import Post


faker = FakerFactory.create()


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    first_name = factory.LazyAttribute(lambda o: faker.first_name())
    last_name = factory.LazyAttribute(lambda o: faker.last_name())
    username = factory.LazyAttribute(lambda o: o.first_name.lower())
    email = factory.LazyAttribute(lambda o: '{0}@{1}'.format(o.username, faker.domain_name()))
    password = factory.PostGenerationMethodCall('set_password', 'password')
    last_login = now()


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.LazyAttribute(lambda o: faker.sentence())
    body = factory.LazyAttribute(lambda o: faker.paragraph())
    author = factory.SubFactory(AuthorFactory)
    publish = now()


class UnpublishedPostFactory(PostFactory):
    publish = now() + timedelta(hours=1)
