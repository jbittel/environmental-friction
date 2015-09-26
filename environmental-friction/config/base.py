from os.path import dirname
from os.path import join

from configurations import Configuration
from configurations import values


BASE_DIR = dirname(dirname(__file__))


class Base(Configuration):
    DJANGO_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    )

    THIRD_PARTY_APPS = (
    )

    LOCAL_APPS = (
        'blog',
    )

    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    )

    DEBUG = values.BooleanValue(False)
    TEMPLATE_DEBUG = DEBUG

    SECRET_KEY = values.SecretValue()

    FIXTURE_DIRS = (
        join(BASE_DIR, 'fixtures'),
    )

    ADMINS = (
        ('Jason Bittel', 'jason.bittel@gmail.com'),
    )
    MANAGERS = ADMINS

    DATABASES = values.DatabaseURLValue('postgres://localhost/friction')

    CACHES = values.CacheURLValue('locmem://')

    TIME_ZONE = 'America/Los_Angeles'

    LANGUAGE_CODE = 'en-us'

    SITE_ID = 1

    USE_I18N = False
    USE_L10N = False
    USE_TZ = True

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.request',
    )

    TEMPLATE_DIRS = (
        join(BASE_DIR, 'templates'),
    )

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

    STATIC_ROOT = join(dirname(BASE_DIR), 'assets')

    STATIC_URL = '/static/'

    STATICFILES_DIRS = ()

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    MEDIA_ROOT = join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

    ROOT_URLCONF = 'urls'

    WSGI_APPLICATION = 'wsgi.application'

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(process)d] [%(levelname)s] %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'django.utils.log.NullHandler',
            },
            'console': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
            },
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
            },
        }
    }

    TEST_RUNNER = 'django.test.runner.DiscoverRunner'

    ALLOWED_HOSTS = ['environmentalfriction.com']

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )
