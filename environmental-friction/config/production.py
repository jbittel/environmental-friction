from .base import Base


class Production(Base):
    SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', Base.TEMPLATE_LOADERS),
    )
