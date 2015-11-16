from django.conf import settings
from storages.backends.s3boto import S3BotoStorage


class StaticStorage(S3BotoStorage):
    location = settings.STATICFILES_PATH


class MediaStorage(S3BotoStorage):
    location = settings.MEDIAFILES_PATH
