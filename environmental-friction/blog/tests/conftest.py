from pytest_factoryboy import register

from .factories import AuthorFactory
from .factories import PostFactory


register(AuthorFactory)
register(PostFactory)
