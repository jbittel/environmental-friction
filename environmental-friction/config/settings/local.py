from .base import *  # noqa


DEBUG = env.bool('DJANGO_DEBUG', default=True)

INSTALLED_APPS += ('debug_toolbar',)
