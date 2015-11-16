from .base import *  # noqa


SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

TEMPLATES[0]['APP_DIRS'] = False
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

INSTALLED_APPS += (
    'storages',
)

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')

STATICFILES_PATH = 'static'
STATICFILES_STORAGE = 'config.s3_storages.StaticStorage'
STATIC_URL = "https://%s.s3.amazonaws.com/%s/" % (AWS_STORAGE_BUCKET_NAME, STATICFILES_PATH)

MEDIAFILES_PATH = 'media'
DEFAULT_FILE_STORAGE = 'config.s3_storages.MediaStorage'
MEDIA_URL = "https://%s.s3.amazonaws.com/%s/" % (AWS_STORAGE_BUCKET_NAME, MEDIAFILES_PATH)
