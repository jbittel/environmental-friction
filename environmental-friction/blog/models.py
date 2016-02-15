from __future__ import unicode_literals

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

import base32_crockford as b32
from taggit.managers import TaggableManager


class PostManager(models.Manager):
    def published(self):
        return self.filter(publish__lte=now())


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
    post_image = models.ImageField(
        verbose_name=_('post image'),
        blank=True,
        upload_to='blog/%Y/%m/%d',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('author'),
        editable=False,
    )
    publish = models.DateTimeField(
        verbose_name=_('publish'),
        blank=True,
        default=now,
        null=True,
    )
    created = models.DateTimeField(
        verbose_name=_('created'),
        editable=False,
    )
    modified = models.DateTimeField(
        verbose_name=_('modified'),
        editable=False,
    )

    objects = PostManager()
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)
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
        return reverse('blog:detail', args=[b32.encode(self.pk), self.slug])

    def get_canonical_url(self):
        return "http://%s%s" % (Site.objects.get_current().domain, self.get_absolute_url())

    def get_status_text(self):
        if self.publish is None:
            return 'Draft'
        elif self.publish > now():
            return 'Scheduled'
        else:
            return 'Published'
