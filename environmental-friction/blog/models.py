from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

import base32_crockford as b32


@python_2_unicode_compatible
class Post(models.Model):
    """
    """
    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
    )
    body = models.TextField(
        verbose_name=_('body'),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('author'),
        editable=False,
    )
    publish = models.DateTimeField(
        verbose_name=_('publish'),
        default=now,
    )
    created = models.DateTimeField(
        verbose_name=_('created'),
        editable=False,
    )
    modified = models.DateTimeField(
        verbose_name=_('modified'),
        editable=False,
    )

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created = now()
        self.modified = now()
        super(Post, self).save(*args, **kwargs)

    @property
    def slug(self):
        return slugify(self.title)

    def get_absolute_url(self):
        return reverse('post-detail', args=[b32.encode(self.pk), self.slug])
