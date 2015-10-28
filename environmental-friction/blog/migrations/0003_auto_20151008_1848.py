# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.sites.models import Site
from django.db import migrations, models


def update_default_site(apps, schema_editor):
    current_site = Site.objects.get_current()
    current_site.domain = 'environmentalfriction.com'
    current_site.name = 'Environmental Friction'
    current_site.save()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20151008_1842'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(update_default_site)
    ]
