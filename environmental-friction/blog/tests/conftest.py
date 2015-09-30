from pytest_factoryboy import register

from .factories import AuthorFactory
from .factories import PostFactory
from .factories import UnpublishedPostFactory


register(AuthorFactory)
register(PostFactory)
register(UnpublishedPostFactory)
