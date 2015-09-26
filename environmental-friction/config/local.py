from configurations import values

from .base import Base


class Local(Base):
    DEBUG = values.BooleanValue(True)

    INSTALLED_APPS = Base.INSTALLED_APPS
    INSTALLED_APPS += ('debug_toolbar',)
